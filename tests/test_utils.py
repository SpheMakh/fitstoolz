import numpy as np
import pytest
from astropy.io import fits
from astropy.wcs import WCS

from fitstoolz.utils import get_beam_table, reorder_wcs

from . import InitTest


@pytest.fixture
def config():
    return InitTest()


def test_reorder_wcs():
    wcs = WCS(naxis=3)
    wcs.wcs.ctype = ["RA---SIN", "DEC--SIN", "FREQ"]
    wcs.wcs.crval = [2.0, -30.0, 1.4e9]
    wcs.wcs.crpix = [64.0, 64.0, 1.0]
    wcs.wcs.cdelt = [-0.001, 0.001, 1e6]
    wcs.wcs.cunit = ["deg", "deg", "Hz"]

    old_order = ["RA---SIN", "DEC--SIN", "FREQ"]
    new_order = ["FREQ", "DEC--SIN", "RA---SIN"]

    result = reorder_wcs(wcs, old_order, new_order)

    assert result.naxis == 3
    assert list(result.wcs.ctype) == new_order
    assert list(result.wcs.crval) == [1.4e9, -30.0, 2.0]
    assert list(result.wcs.cdelt) == [1e6, 0.001, -0.001]
    assert list(result.wcs.cunit) == ["Hz", "deg", "deg"]


def test_get_beam_table_bintable(config: InitTest):
    pix_size = 5 / 3600
    npix = 64
    wcs = WCS(naxis=3)
    wcs.wcs.ctype = ["RA---SIN", "DEC--SIN", "FREQ"]
    wcs.wcs.cdelt = np.array([-pix_size, pix_size, 1e6])
    wcs.wcs.crpix = [npix / 2, npix / 2, 1]
    wcs.wcs.crval = [2.0, -30, 1.4e9]
    wcs.wcs.cunit = ["deg", "deg", "Hz"]
    header = wcs.to_header()

    image = np.zeros((1, npix, npix), dtype=np.float32)
    phdu = fits.PrimaryHDU(image, header=header)

    from astropy.table import Table

    beam_tab = Table(
        {
            "BMAJ": [0.1],
            "BMIN": [0.05],
            "BPA": [30.0],
        }
    )
    beam_hdu = fits.BinTableHDU(beam_tab)
    hdul = fits.HDUList([phdu, beam_hdu])

    fname = config.random_named_file(suffix=".fits")
    hdul.writeto(fname, overwrite=True)

    result = get_beam_table(fname)
    assert result is not False
    assert result["BMAJ"][0] == 0.1
    assert result["BMIN"][0] == 0.05
    assert result["BPA"][0] == 30.0


def test_get_beam_table_header(config: InitTest):
    pix_size = 5 / 3600
    npix = 64
    wcs = WCS(naxis=3)
    wcs.wcs.ctype = ["RA---SIN", "DEC--SIN", "FREQ"]
    wcs.wcs.cdelt = np.array([-pix_size, pix_size, 1e6])
    wcs.wcs.crpix = [npix / 2, npix / 2, 1]
    wcs.wcs.crval = [2.0, -30, 1.4e9]
    wcs.wcs.cunit = ["deg", "deg", "Hz"]
    header = wcs.to_header()
    header["BMAJ"] = 0.2
    header["BMIN"] = 0.1
    header["BPA"] = 45.0

    image = np.zeros((1, npix, npix), dtype=np.float32)
    hdu = fits.PrimaryHDU(image, header=header)
    hdul = fits.HDUList([hdu])

    fname = config.random_named_file(suffix=".fits")
    hdul.writeto(fname, overwrite=True)

    result = get_beam_table(fname)
    assert result is not False
    assert result["BMAJ"][0] > 0
    assert result["BPA"][0] > 0


def test_get_beam_table_missing_file():
    with pytest.raises(FileNotFoundError):
        get_beam_table("/nonexistent/file.fits")
