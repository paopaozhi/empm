import typer
import logging
from rich.logging import RichHandler
from rich.console import Console
import random
from rich.progress import Progress
from rich.progress import TimeElapsedColumn,SpinnerColumn
import time

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

app = typer.Typer()

@app.callback(invoke_without_command=True)
def install():
    console = Console(record=True)
    
    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        transient=False,
    ) as progress:
        task1 = progress.add_task("[red]Downloading", total=100)
        task2 = progress.add_task("[green]Processing", total=100)
        # task3 = progress.add_task("[yellow]Thinking", total=None)
        
        log.debug("start")
        try:
            while not progress.finished:
                progress.update(task1, advance=0.5)
                progress.update(task2, advance=0.3)
                time.sleep(0.01)
                if random.randint(0, 100) < 1:
                    log.info("123")
                    progress.log(123)
        except:
            log.info("end")
    
@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")
      
@app.command()
def init():
    print("default")
        
def run():
    app()
    
if __name__ == "__main__":
    run()