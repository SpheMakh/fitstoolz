import os.path
import shutil
import tempfile

from astropy.utils.data import download_file

TESTDIR = os.path.abspath(os.path.dirname(__file__))

class InitTest:
    def __init__(self):
        self.test_files = []

    def astropy_example_image(self, fname=None):
        fname = fname or "HorseHead.fits"
        image_file = download_file(f"http://data.astropy.org/tutorials/FITS-images/{fname}")
        self.test_files.append(image_file)
        return image_file

    def random_named_file(self, suffix: str = None):
        if not hasattr(self, "test_files"):
            self.test_files = []

        file_obj = tempfile.NamedTemporaryFile(suffix=suffix, dir=TESTDIR, delete_on_close=False)
        name = file_obj.name
        file_obj.close()

        self.test_files.append(name)
        return name

    def random_named_directory(self, suffix: str = None):
        if not hasattr(self, "test_files"):
            self.test_files = []

        dir_obj = tempfile.TemporaryDirectory(suffix=suffix, dir=TESTDIR, delete=False)
        name = dir_obj.name

        self.test_files.append(name)
        return name

    def __del__(self):
        for path in getattr(self, "test_files", []):
            if os.path.exists(path):
                if os.path.isfile(path):
                    try:
                        os.remove(path)
                    except OSError as e:
                        print(f"Error deleting file '{path}': {e}")
                elif os.path.isdir(path):
                    try:
                        shutil.rmtree(path)
                    except OSError as e:
                        print(f"Error deleting directory '{path}': {e}")