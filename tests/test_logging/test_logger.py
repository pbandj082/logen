from logen import (
    LoggingFactory,
    Level,
)
from logen.formatter import ConsoleMessage, ForeColoring, ConsoleColors

def test_default_format():
    logen_factory = LoggingFactory()
    logger = logen_factory.acquire_logger(__name__)
    logen_factory.create_console_handler()
    logger.set_level(Level.debug)
    console_log_handler = logen_factory.create_console_handler()
    console_log_handler.set_level(Level.debug)
    debug_file_log_handler = logen_factory.create_file_handler('tests/test_logging/log/debug.log')
    debug_file_log_handler.set_level(Level.debug)
    error_file_log_handler = logen_factory.create_file_handler('tests/test_logging/log/error.log')
    error_file_log_handler.set_level(Level.error)
    logger.add_handler(debug_file_log_handler)
    logger.add_handler(error_file_log_handler)
    logger.add_handler(console_log_handler)
    logger.debug('This is debug log.')
    coloring_info_str = ForeColoring(
        child=ConsoleMessage("info"),
        color=ConsoleColors.bright_green,
    ).sequence_string()
    logger.info('This is info log.', console_msg=f'This is {coloring_info_str} log')
    logger.warning('This is warning log.')
    logger.error('This is error log.')
    logger.critical('This is critical log.')
