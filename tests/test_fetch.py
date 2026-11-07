import hashlib
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec=importlib.util.spec_from_file_location('fetch',Path(__file__).resolve().parents[1]/'scripts/fetch.py')
fetch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch)

class DownloadIntegrity(unittest.TestCase):
    def test_download_and_corrupt_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'source';source.write_bytes(b'dataset-check\n')
            expected=dict(bytes=source.stat().st_size,sha256=hashlib.sha256(source.read_bytes()).hexdigest())
            fetch.download(source.as_uri(),root/'target',expected)
            self.assertEqual(source.read_bytes(),(root/'target').read_bytes())
            with self.assertRaises(ValueError):
                fetch.download(source.as_uri(),root/'bad',dict(bytes=expected['bytes'],sha256='0'*64))
            with self.assertRaises(ValueError):
                fetch.download(source.as_uri(),root/'short',dict(bytes=expected['bytes']+1,sha256=expected['sha256']))

if __name__=='__main__':unittest.main()
