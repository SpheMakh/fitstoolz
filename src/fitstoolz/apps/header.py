import click
from astropy.io import fits
from omegaconf import OmegaConf
from scabha.schema_utils import clickify_parameters

from . import get_app_config

app = "header"


@click.command(app)
@clickify_parameters(get_app_config(app))
def runit(**kwargs):
    opts = OmegaConf.create(kwargs)
    if opts.show:
        with fits.open(opts.fname) as hdul:
            print(repr(hdul[0].header))
        return

    outfile = None
    if opts.outfile:
        outfile = opts.outfile
    elif opts.replace:
        outfile = opts.fname

    if outfile is None:
        raise RuntimeError("Neither --replace nor --outfile is set. Cannot add/remove/edit.")

    updates = {}
    hdul = fits.open(opts.fname)

    if opts.edit or opts.add:
        if opts.edit:
            keyvals = opts.edit
        else:
            keyvals = opts.add

        for keyval in keyvals:
            key, strval = keyval.split("=", 1)
            key = key.strip()
            strval = strval.strip()

            try:
                val = int(strval)
            except ValueError:
                try:
                    val = float(strval)
                except ValueError:
                    val = strval

            updates[key] = val
        hdul[0].header.update(updates)

    elif opts.remove:
        for key in opts.remove:
            del hdul[0].header[key]

    hdul.writeto(outfile, overwrite=True)

    hdul.close()
