import click
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from fitstoolz import set_logger
from fitstoolz.apps import get_app_config, outfits_name
from fitstoolz.reader import FitsData

app = "add-axis"


@click.command(app)
@clickify_parameters(get_app_config(app))
@click.pass_context
def runit(ctx, **kwargs):
    opts = OmegaConf.create(kwargs)

    log = set_logger("fitstoolz", level=ctx.obj["log_level"])
    outfits = outfits_name(opts.fname, opts.outfile, opts.replace, raise_exception=True)

    with FitsData(fname=opts.fname, memmap=True) as myfits:
        if opts.ctype in myfits.coord_names:
            raise ValueError(f"Axis '{opts.ctype}' already exists.")

        myfits.add_axis(
            name=opts.ctype, idx=opts.index, crval=opts.crval, cdelt=opts.cdelt, crpix=opts.crpix, cunit=opts.cunit
        )

        chunks = myfits.build_chunks(
            ra_chunks=opts.ra_chunks, dec_chunks=opts.dec_chunks, spectral_chunks=opts.spectral_chunks
        )
        myfits.write_to_fits(outfits, chunks=chunks)

    log.info(f"Finished. File written to: {outfits}")
