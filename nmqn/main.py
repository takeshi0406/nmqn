import click
from nmqn import crawl as c

@click.group()
def cmd():
    pass

@cmd.command()
@click.option('config', '-c', required=True, type=str, help='Chrome Tab')
@click.option('max_tab', '-m', default=10, type=int, help='Chrome Tab')
@click.option('--debug', is_flag=True, help='headless mode')
def crawl(config, max_tab, debug):
    c.execute(config, max_tab, not debug)

def main():
    cmd()

if __name__ == "__main__":
    main()