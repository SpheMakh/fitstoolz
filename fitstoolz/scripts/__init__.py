import glob
import os.path

from scabha.basetypes import File

thisdir = os.path.dirname(__file__)
source_files = glob.glob(f"{thisdir}/cabs/*.yaml")
sources = [File(item) for item in source_files]
