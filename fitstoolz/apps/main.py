import click

from .lazy_group import LazyGroup

applist = "remove_axis add_axis unstack stack slice stats header".split()
app_dict = dict([(name.replace("_","-"), f"{name}.runit") for name in applist])

@click.group(
        cls=LazyGroup,
        lazy_subcommands=app_dict, 
        parent_module="fitstoolz.apps"
)
def cli():
    pass

