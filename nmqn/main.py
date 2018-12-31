import click
from nmqn import crawl as c

@click.group()
def cmd():
    pass

@cmd.command()
@click.option('config', '-c', required=True, type=str, help='Config path.')
@click.option('max_tab', '-m', default=10, type=int, help='Chrome Tab.')
@click.option('path', '-p', default="./.tmp", type=str, help='OutputPath')
@click.option('--debug', is_flag=True, help='not headless mode')
def crawl(config, max_tab, path, debug):
    c.execute(config, max_tab, path, not debug)

def main():
    cmd()

if __name__ == "__main__":
    main()