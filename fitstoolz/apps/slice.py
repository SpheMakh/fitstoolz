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
        coord_names = list(myfits.coord_names)
        slc = [slice(None)] * myfits.ndim

        if opts.axis:
            for axspec in opts.axis:
                ctype, start, end = str(axspec).split(",")
                start = int(start)
                end = int(end)
                if ctype not in coord_names:
                    raise ValueError(f"Unknown axis '{ctype}'. Existing axes are: {coord_names}")
                idx = coord_names.index(ctype)
                slc[idx] = slice(start, end)

        chunks = myfits.build_chunks(
            ra_chunks=opts.ra_chunks, dec_chunks=opts.dec_chunks, spectral_chunks=opts.spectral_chunks
        )
        myfits.write_to_fits(outfits, coord_names=coord_names, data_slice=slc, chunks=chunks)
