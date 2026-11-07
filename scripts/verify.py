#!/usr/bin/env python3
"""Verify extracted source bytes and independently check published result populations."""
import csv
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text())


def ledger(path):
    requests={}; phases={}
    with path.open() as f:
        for line in f:
            text=line.strip()
            if not text: continue
            if not text.startswith('{'):
                start=text.index('msg="')+4
                text,_=json.JSONDecoder().raw_decode(text[start:])
            event=json.loads(text)
            if event['t']=='origin': continue
            key=event['id']; phase=event['phase']
            if event['t']=='send':
                assert key not in requests, 'Duplicate request'
                requests[key]=[phase,False]
                phases.setdefault(phase,dict(sent=0,correct=0,onTime=0,durations=[]))['sent']+=1
            else:
                assert event['t'] in ('done','error','timeout')
                assert key in requests and requests[key]==[phase,False], 'Invalid terminal event'
                requests[key][1]=True
                if event.get('ok'):
                    p=phases[phase];p['correct']+=1;p['durations'].append(event['dur'])
                    p['onTime']+=event.get('wallMs',math.inf)<=500
    return phases


def q(values, fraction):
    return sorted(values)[max(0,math.ceil(len(values)*fraction)-1)]


def verify_qr(root):
    computed={}
    for run in read(root/'run-index.json'):
        base=root/'raw/runs'/run['id']
        path=base/'events.log' if run['platform'].startswith('nanofaas') else base/'attempts/1/k6-events.jsonl'
        phases=ledger(path)
        if run['platform'].startswith('nanofaas'):
            expected=read(base/'summary.json')['phases']
            rates={p['phase']:p['offered'] for p in expected}
        elif run['platform']=='spin':
            expected=list(csv.DictReader((root/f"derived/spin-rate{run['finalRate']}-phases.csv").open()))
            rates={p['phase']:float(p['offeredRate']) for p in expected}
        else:
            expected=[p for p in csv.DictReader((root/'derived/baseline-phases.csv').open())
                      if p['configuration']==run['platform'] and int(p['repetition'])==run['repetition']]
            rates={p['phase']:float(p['offeredRate']) for p in expected}
        for p in expected:
            if not rates[p['phase']]: continue
            actual=phases[p['phase']]
            assert actual['sent']==int(p['sent']) and actual['correct']==int(p['correct'])
            for percentile in (50,95):
                assert math.isclose(q(actual['durations'],percentile/100),float(p[f'p{percentile}Ms']),abs_tol=1e-9)
            computed[(run['id'],rates[p['phase']])]=actual
    points=read(root/'derived/figure-points.json')['points']
    assert len(points)==104
    for p in points:
        platform=p['platform'].replace('p1-','nanofaas-')
        key=f"spin-rate{p['run']}-r1" if platform=='spin' else f"{platform}-r{p['run']}"
        actual=computed[(key,p['offered'])]
        assert math.isclose(actual['correct']/120,p['correctPerSecond'],abs_tol=1e-9)
    table=read(root/'derived/table-values.json')['rows']
    for row in table:
        platform=row['label'].lower().replace('p1 ','nanofaas-')
        ids=[f'spin-rate{int(row["rate"])}-r1'] if platform=='spin' else [f'{platform}-r{n}' for n in (1,2,3)]
        values=[computed[(i,row['rate'])] for i in ids]
        for percentile in (25,50,95):
            mean=statistics.mean(q(r['durations'],percentile/100) for r in values)
            assert math.isclose(mean,row[f'p{percentile}Ms'],abs_tol=1e-9)
        assert math.isclose(statistics.mean(r['correct']/120 for r in values),row['goodput'],abs_tol=1e-9)
        assert math.isclose(statistics.mean(100*r['correct']/r['sent'] for r in values),row['successPercent'],abs_tol=1e-9)
    return dict(runs=25,figurePoints=len(points),tableRows=len(table),latencyPercentiles=[25,50,95])


def verify_results(root):
    name=root.name
    if name.startswith('01-'):
        blocks=read(root/'derived/verified.json')
        assert len(blocks)==3 and all(len(b['arms'])==8 and not b['errors'] for b in blocks)
        for i,b in enumerate(blocks,1):
            original=read(root/f'raw/block-{i}/analysis.json')
            assert original==b
        return dict(blocks=3,arms=24)
    if name.startswith('02-'): return verify_qr(root)
    if name.startswith('03-'):
        rows=read(root/'derived/evaluation-results.json')
        assert len(rows)==24
        for r in rows.values():
            run=root/'raw/evaluation'/Path(r['path']).name
            phases=ledger(run/'events.log')
            for p in r['summary']['phases']:
                for key in ('sent','correct','onTime'):
                    assert phases[p['phase']][key]==p[key]
        groups=read(root/'derived/data.json')['groups']
        for g in groups:
            selected=[r for r in rows.values() if r['cell']['scenario']==g['scenario'] and r['cell']['policy']==g['policy']]
            assert len(selected)==3
            for metric in ('onTimeFraction','correctFraction'):
                values=[r['summary']['total'][metric] for r in selected]
                for key,fn in [('mean',statistics.mean),('min',min),('max',max)]:
                    assert math.isclose(fn(values),g[metric][key],abs_tol=1e-12)
        assert len(list((root/'raw/calibration').iterdir()))==4
        return dict(evaluationRuns=24,calibrationRuns=4)
    if name.startswith('04-'):
        cycles=list(csv.DictReader((root/'derived/cycles.csv').open()))
        assert len(cycles)==30
        assert len({(r['runtime'],r['treatment']) for r in cycles})==10
        return dict(configurations=10,idleCycles=30)
    if name.startswith('05-'):
        arms=read(root/'derived/rates20-300.json')['arms']+read(root/'derived/rates400-500.json')['arms']
        assert len(arms)==15
        for a in arms:
            name=f"{a['mode']}-r{a['rate']}"
            assert (root/'raw/runs'/name/'results/k6-events.jsonl').is_file()
        for mode,refused in [('disabled',19),('pressure',1),('cloud',740)]:
            row=next(a for a in arms if a['rate']==500 and a['mode']==mode)
            assert row['outcomes']['refused']==refused
        return dict(arms=15,rates=[20,100,300,400,500])
    if name.startswith('06-'):
        forecasts=list(csv.DictReader((root/'derived/forecasts.csv').open()))
        assert len(forecasts)==5400
        summary=read(root/'derived/summary.json')
        for name in ('Oracle','ARI'):
            assert len([r for r in forecasts if r['run']==name])==2700
            assert sum(summary['runs'][name]['counts'].values())==142242
        for name in ('continuous-oracle','continuous-ari-history-fix'):
            assert (root/'raw'/name/'run/generator.jsonl').is_file()
            assert (root/'raw'/name/'freeze/selected.json').is_file()
        return dict(runs=2,epochsPerRun=54,forecastCellsPerRun=2700,edgeRequestsPerRun=142242)
    raise ValueError(name)


def main():
    root=Path(sys.argv[1]).resolve()
    manifest=read(root/'source-files.json')
    for relative,meta in manifest.items():
        p=root/relative
        assert p.resolve().is_relative_to(root) and not p.is_symlink()
        assert p.stat().st_size==meta['bytes'] and digest(p)==meta['sha256'], relative
    print(json.dumps(dict(experiment=root.name,verifiedFiles=len(manifest),results=verify_results(root))))


if __name__=='__main__':
    assert q([4,1,3,2],.25)==1 and q([5,4,1,3,2],.25)==2
    main()
