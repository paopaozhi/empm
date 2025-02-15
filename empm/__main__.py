import sys

if len(sys.argv) == 1:
    print("usage: python -m empm")
else:
    from ._internal.cli.main import app
    app()
