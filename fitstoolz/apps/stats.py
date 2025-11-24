import click
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
        log.info(f"Data standard deviation: {myfits.data.std().compute()}")
