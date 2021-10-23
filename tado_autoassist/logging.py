import logging
from os import PathLike
from typing import Optional


def configure_logging(log_file_name: Optional[str | PathLike[str]] = None):
    handlers = [logging.StreamHandler()]
    if log_file_name is not None:
        handlers.append(logging.FileHandler(log_file_name))

    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers,
    )

    library_name = __name__.split('.')[0]
    logging.getLogger(library_name).setLevel(logging.INFO)
