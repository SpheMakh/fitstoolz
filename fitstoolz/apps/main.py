import click


@click.group()
def cli():
    pass


applist = "remove_axis add_axis unstack stack slice stats header".split()
apps = __import__("fitstoolz.apps", fromlist=applist)

for app in applist:
    cli.add_command(getattr(apps, app).runit)
