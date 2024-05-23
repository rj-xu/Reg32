import logging
import time

import colorlog

LOG_PATH = "./a.log"
LOG_LEVEL = logging.DEBUG


# _FMT = "[%(asctime)s][%(levelname)-8s] %(message)s"
_DEBUG_INFO = " (%(filename)s:%(lineno)s %(funcName)s)"
_FMT_DICT = {
    # fmt: off
    "DEBUG"    : "%(log_color)s[%(asctime)s][DEBUG] %(message)s"    + _DEBUG_INFO,
    "INFO"     : "%(log_color)s[%(asctime)s][INFO ] %(message)s"                 ,
    "WARNING"  : "%(log_color)s[%(asctime)s][WARN ] %(message)s"    + _DEBUG_INFO,
    "ERROR"    : "%(log_color)s[%(asctime)s][ERROR] %(message)s"    + _DEBUG_INFO,
    "CRITICAL" : "%(log_color)s[%(asctime)s][CRITICAL] %(message)s" + _DEBUG_INFO,
    # fmt: on
}
_DATEFMT = "%Y-%m-%d %H:%M:%S"

TEST_TIME = time.strftime(_DATEFMT)
LINE = "=" * 50

g_logger = logging.getLogger()


_g_stream_formatter = colorlog.LevelFormatter(
    fmt=_FMT_DICT,
    datefmt=_DATEFMT,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red,bg_white",
    },
)
_g_stream_handler = logging.StreamHandler()
_g_stream_handler.setFormatter(_g_stream_formatter)
g_logger.addHandler(_g_stream_handler)

_g_file_formatter = colorlog.LevelFormatter(
    fmt=_FMT_DICT,
    datefmt=_DATEFMT,
    no_color=True,
)
_g_file_handler = logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8")
_g_file_handler.setFormatter(_g_file_formatter)
g_logger.addHandler(_g_file_handler)

g_logger.setLevel(LOG_LEVEL)

# g_logger.debug("This is Debug")
# g_logger.info("This is Info")
# g_logger.warning("This is Warning")
# g_logger.error("THIS IS ERROR")
# g_logger.critical("THIS IS CRITICAL")

g_logger.info(f"{LINE} Test Start {LINE}")
g_logger.info(f"Test    Time   : {TEST_TIME}")
g_logger.info(f"Log     Path   : {LOG_PATH}")
g_logger.info(f"Program Version: {None}")
g_logger.info(f"Device  Version: {None}")
g_logger.info(f"Board   Version: {None}")
g_logger.info(f"FW      Version: {None}")
g_logger.info(f"{LINE}============{LINE}")
