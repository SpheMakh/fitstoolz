import click
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from fitstoolz import set_logger
from fitstoolz.apps import get_app_config, outfits_name
from fitstoolz.reader import FitsData

app = "remove-axis"


@click.command(app)
@clickify_parameters(get_app_config(app))
@click.pass_context
def runit(ctx, **kwargs):
    opts = OmegaConf.create(kwargs)

    log = set_logger("fitstoolz", level=ctx.obj["log_level"])
    outfits = outfits_name(opts.fname, opts.outfile, opts.replace, raise_exception=True)

    with FitsData(fname=opts.fname, memmap=True) as myfits:
        coord_names = myfits.coord_names
        if opts.ctype not in coord_names:
            raise ValueError(f"Unknown axis '{opts.ctype}'. Existing axes are: {coord_names}")

        idx = coord_names.index(opts.ctype)
        coord_names.pop(idx)
        slc = [slice(None)] * myfits.ndim
        slc[idx] = opts.select_index

        chunks = myfits.build_chunks(
            ra_chunks=opts.ra_chunks, dec_chunks=opts.dec_chunks, spectral_chunks=opts.spectral_chunks
        )
        myfits.write_to_fits(outfits, coord_names=coord_names, data_slice=slc, chunks=chunks)

    log.info(f"Finished. File written to: {outfits}")
