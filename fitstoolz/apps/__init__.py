import os.path

from scabha.basetypes import File
from scabha.schema_utils import paramfile_loader

thisdir = os.path.dirname(__file__)
config_dir = os.path.join(thisdir, "parser_configs")

sources = [File(os.path.join(config_dir, "base.yaml"))]


def get_app_config(app):
    parserfile = File(f"{config_dir}/{app}.yaml")
    return paramfile_loader(parserfile, sources, use_cache=False)[app]


def outfits_name(infile, outfile, replace=False, raise_exception=False):
    if outfile:
        return outfile
    elif replace:
        return infile
    else:
        if raise_exception:
            raise RuntimeError("Both --replace and --outfile are not set. Cannot modify FITS file(s).")
        else:
            return None
