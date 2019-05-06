import zipfile
import os
import time
import datetime
import struct
import contextlib

PYC_TIMESTAMP = datetime.date(1981, 1, 1)
PYC_UNIX_TIMESTAMP = struct.pack("I", int(time.mktime(PYC_TIMESTAMP.timetuple())))


@contextlib.contextmanager
def createzip(zipfile_path):
    with zipfile.ZipFile(zipfile_path + ".tmp", "w", compression=zipfile.ZIP_DEFLATED) as zipper:
        def _add_to_zip(name, contents):
            if name.endswith(".pyc"):
                assert len(PYC_UNIX_TIMESTAMP) == 4
                contents = contents[:4] + PYC_UNIX_TIMESTAMP + contents[8:]
            info = zipfile.ZipInfo(filename=name, date_time=(1980, 1, 1, 0, 0, 0))
            zipper.writestr(info, contents, compress_type=zipfile.ZIP_DEFLATED)
        yield _add_to_zip
    os.rename(zipfile_path + ".tmp", zipfile_path)
