import click
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from fitstoolz import set_logger
from fitstoolz.reader import FitsData

from . import get_app_config

app = "stack"


@click.command(app)
@clickify_parameters(get_app_config(app))
@click.pass_context
def runit(ctx, **kwargs):
    opts = OmegaConf.create(kwargs)

    log = set_logger("fitstoolz", level=ctx.obj["log_level"])

    fname0 = opts.fname
    fnames = opts.extra_files or []

    with FitsData(fname=fname0, memmap=True) as myfits:
        myfits.expand_along_axis_from_files(opts.axis, fnames)
        chunks = myfits.build_chunks(
            ra_chunks=opts.ra_chunks, dec_chunks=opts.dec_chunks, spectral_chunks=opts.spectral_chunks
        )
        myfits.write_to_fits(opts.stacked_fits, chunks=chunks)

    log.info(f"Wrote stacked file to: {opts.stacked_fits}")
