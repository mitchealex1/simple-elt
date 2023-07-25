"""CLI"""

import pathlib
import click

from backend import Backend


@click.group()
@click.pass_context
@click.option("--postgres-user", type=str)
@click.option("--postgres-password", type=str)
@click.option("--postgres-host", type=str)
@click.option("--postgres-port", type=int)
@click.option("--postgres-database", type=str)
@click.option("--postgres-schema", type=str)
@click.option(
    "--data-directory",
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
)
def cli(*args, **kwargs):
    """Tool to load and unload the Facebook datasets to and from the database"""
    ctx = args[0]
    ctx.ensure_object(dict)
    ctx.obj["handler"] = Backend(kwargs)


@cli.command("load")
@click.pass_obj
@click.argument("dataset", type=click.Choice(["messages", "friends_and_followers"]))
def load(ctx_obj: dict, dataset: str):
    """Load a dataset into the database"""
    handler = ctx_obj["handler"]
    handler.execute(dataset, "load")


@cli.command("unload")
@click.pass_obj
@click.argument("dataset", type=click.Choice(["messages", "friends_and_followers"]))
def unload(ctx_obj: dict, dataset: str):
    """Unload a dataset from the database"""
    handler = ctx_obj["handler"]
    handler.execute(dataset, "unload")


if __name__ == "__main__":
    cli(auto_envvar_prefix="LOAD")
