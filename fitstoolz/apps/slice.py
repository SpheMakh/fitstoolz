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

    outfits = outfits_name(opts.fname, opts.outfile, replace=opts.replace, raise_exception=True)

    with FitsData(fname=opts.fname, memmap=opts.memmap) as myfits:
        chunks = myfits.build_chunks(
            ra_chunks=opts.ra_chunks, dec_chunks=opts.dec_chunks, spectral_chunks=opts.spectral_chunks
        )
        myfits.write_to_fits(outfits, coord_names=myfits.coord_names, chunks=chunks)
