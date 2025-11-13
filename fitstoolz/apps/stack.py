import click
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from fitstoolz import LOG
from fitstoolz.reader import FitsData

from . import get_app_config

app = "stack"


@click.command(app)
@clickify_parameters(get_app_config(app, add_sources=["unstack"]))
def runit(**kwargs):
    opts = OmegaConf.create(kwargs)

    fname0 = opts.fname[0]
    fnames = opts.fname[1:]
    myfits = FitsData(fname=fname0, memmap=opts.memmap)

    myfits.expand_along_axis_from_files(opts.axis, fnames)
    coord_names = myfits.coord_names
    spectral = myfits.spectral_coord
    chunks = {
        "RA": opts.ra_chunks,
        "DEC": opts.dec_chunks,
        spectral: opts.spectral_chunks,
    }

    myfits.write_to_fits(opts.stacked_fits, coord_names=coord_names, chunks=chunks)
    LOG.info(f"Wrote stacked file to: {opts.stacked_fits}")
