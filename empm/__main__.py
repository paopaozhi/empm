import sys

if len(sys.argv) == 1:
    print("usage: python -m empm")
else:
    from .cli.main import app

    app()
