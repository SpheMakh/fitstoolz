import click
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from . import get_app_config

app = "remove-axis"


@click.command(app)
@clickify_parameters(get_app_config(app))
def runit(**kwargs):
    opts = OmegaConf(kwargs)
    opts.fname
