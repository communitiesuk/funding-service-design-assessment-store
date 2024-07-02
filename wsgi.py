import os
from pathlib import Path

from app import app

if __name__ == "__main__":
    if (
        # The WERKZEUG_RUN_MAIN is set to true when running the subprocess for
        # reloading, we want to start debugpy only once during the first
        # invocation and never during reloads.
        os.environ.get("WERKZEUG_RUN_MAIN")
        != "true"
    ):
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        debugpy.wait_for_client()

    app.run(f"{Path(__file__).stem}:app")
