import click
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from fitstoolz.reader import FitsData

from . import get_app_config, outfits_name

app = "slice"


@click.command(app)
@clickify_parameters(get_app_config(app))
def runit(**kwargs):
    opts = OmegaConf.create(kwargs)

    myfits = FitsData(fname=opts.fname, memmap=opts.memmap)
    outfits = outfits_name(opts.fname, opts.outfile, replace=opts.replace, raise_exception=True)

    coord_names = myfits.coord_names
    spectral = myfits.spectral_coord
    chunks = {
        "RA": opts.ra_chunks,
        "DEC": opts.dec_chunks,
        spectral: opts.spectral_chunks,
    }

    myfits.write_to_fits(outfits, coord_names=coord_names, chunks=chunks)


#    LOG.info(f"Wrote stacked file to: {opts.stacked_fits}")
