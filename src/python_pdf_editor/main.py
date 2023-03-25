import argparse
from python_pdf_editor.app import app


def main() -> None:
    """
    The core function of this awesome project.
    """

    # starting the dash app
    app.run_server()


if __name__ == "__main__":
    main()
