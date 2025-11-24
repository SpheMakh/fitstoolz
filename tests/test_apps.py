import pytest
from click.testing import CliRunner

from fitstoolz.apps import main as main_group

from . import InitTest


@pytest.fixture
def config():    
    return InitTest()


def test_help_display():
    runner = CliRunner()
    result = runner.invoke(main_group.cli, ["--help"])
    assert result.exit_code == 0
    for app in main_group.app_dict:
        result = runner.invoke(main_group.cli, [app, "--help"])
        assert result.exit_code == 0


def test_header(config):
    image_file = config.astropy_example_image()
    runner = CliRunner()

    result = runner.invoke(main_group.cli,
                f"header --show {image_file}".split())
    assert result.exit_code == 0

    outfits = config.random_named_file(suffix=".fits")
    result = runner.invoke(main_group.cli,
                f"header --add Foo=bar --outfile {outfits} {image_file}")

    assert result.exit_code == 0

    result = runner.invoke(main_group.cli,
                f"header --edit Foo=23 --outfile {outfits} {image_file}")
    
    assert result.exit_code == 0
    
    result = runner.invoke(main_group.cli,
                f"header --remove Foo --replace {outfits}")
    
    assert result.exit_code == 0
