from pathlib import Path

import logging


log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)


def get_logger(name: str = 'app') -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt='[%(asctime)s.%(msecs)03d] - %(name)s:%(lineno)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    app_handler = logging.FileHandler(f'{log_dir}/app.log', mode='a', encoding='utf-8')
    app_handler.setLevel(logging.DEBUG)
    app_handler.setFormatter(formatter)

    errors_handler = logging.FileHandler(
        f'{log_dir}/errors.log', mode='a', encoding='utf-8'
    )
    errors_handler.setLevel(logging.ERROR)
    errors_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(app_handler)
    logger.addHandler(errors_handler)
    logger.addHandler(console_handler)


    return logger
