"""Command line interface for `test_repo`."""

import click


@click.command()
@click.option('--name', default='world', help='Who to greet.')
def main(name: str) -> None:
    """Greet someone.

    Arguments:
        name: Who to greet.
    """
    click.echo(f'Hello, {name}!')


if __name__ == '__main__':
    main()
