from loguru import logger
from pathlib import Path
import sys


def setup_logger(
    name: str = "app",
    console_level: str = "DEBUG",
    file_level: str = "ERROR",
    log_file: str = "logs/app.log",
    rotation: str = "5 MB",
    retention: int = 5,
):
    """
    Configure Loguru logger with console + rotating file output.
    """

    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    # Remove default handler to prevent duplicates
    logger.remove()

    # === Console Handler (Human Readable) ===
    logger.add(
        sys.stdout,
        level=console_level,
        format="{time:YYYY-MM-DD HH:mm:ss} - {name} - {level} - {message}",
        colorize=True,
    )

    # === File Handler (Structured JSON) ===
    logger.add(
        log_file,
        level=file_level,
        rotation=rotation,
        retention=retention,
        format=(
            "{{"
            "'time':'{time:YYYY-MM-DD HH:mm:ss}', "
            "'name':'{name}', "
            "'level':'{level}', "
            "'message':'{message}'"
            "}}"
        ),
        serialize=False,  # set True if you want real JSON
    )

    # Bind app name (optional metadata)
    return logger.bind(app=name)


def get_logger():
    """
    Return the global Loguru logger.
    """
    return logger
