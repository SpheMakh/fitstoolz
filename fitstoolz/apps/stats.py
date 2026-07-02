import click
import dask.array as da
import numpy as np
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from fitstoolz import set_logger
from fitstoolz.apps import get_app_config
from fitstoolz.reader import FitsData

app = "stats"


@click.command(app)
@clickify_parameters(get_app_config(app))
@click.pass_context
def runit(ctx, **kwargs):
    opts = OmegaConf.create(kwargs)

    log = set_logger("fitstoolz", level=ctx.obj["log_level"])

    with FitsData(fname=opts.fname, memmap=True) as myfits:
        data = myfits.data

        slc = [slice(None)] * myfits.ndim
        if opts.slice:
            for axspec in opts.slice:
                ctype, start, end = str(axspec).split(",")
                start = int(start)
                end = int(end)
                if ctype not in myfits.coord_names:
                    raise ValueError(f"Unknown axis '{ctype}'. Existing axes are: {myfits.coord_names}")
                idx = myfits.coord_names.index(ctype)
                slc[idx] = slice(start, end)
        data = data[tuple(slc)]

        if opts.clip_below is not None:
            blank = opts.blank_value if opts.blank_value is not None else np.nan
            data = da.where(data < opts.clip_below, blank, data)
        if opts.clip_above is not None:
            blank = opts.blank_value if opts.blank_value is not None else np.nan
            data = da.where(data > opts.clip_above, blank, data)

        if opts.show:
            log.info(
                f"min={data.min().compute():.6g}  max={data.max().compute():.6g}  "
                f"mean={data.mean().compute():.6g}  std={data.std().compute():.6g}"
            )
        else:
            log.info(f"Data standard deviation: {data.std().compute()}")
