import logging
import pytest
from logen import (
    LoggingFactory,
    Logger,
    Level,
    standard_console_log_format_function,
    standard_file_log_format_function
)

def test_default_format():
    logen_factory = LoggingFactory()
    logger = logen_factory.get_logger(__name__)
    logen_factory.create_console_handler()
    logger.set_level(Level.debug)
    console_log_handler = logen_factory.create_console_handler()
    console_log_handler.set_level(Level.debug)
    console_log_formatter = logen_factory.create_formatter(standard_console_log_format_function)
    console_log_handler.set_formatter(console_log_formatter)
    debug_file_log_handler = logen_factory.create_file_handler('tests/test_logging/log/debug.log')
    debug_file_log_handler.set_level(Level.debug)
    error_file_log_handler = logen_factory.create_file_handler('tests/test_logging/log/error.log')
    error_file_log_handler.set_level(Level.error)
    file_log_formatter = logen_factory.create_formatter(standard_file_log_format_function)
    debug_file_log_handler.set_formatter(file_log_formatter)
    error_file_log_handler.set_formatter(file_log_formatter)
    logger.add_handler(debug_file_log_handler)
    logger.add_handler(error_file_log_handler)
    logger.add_handler(console_log_handler)
    logger.debug('This is debug log.')
    logger.error('This is error log.')
