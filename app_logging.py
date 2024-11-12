
import logging, sys

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set the minimum level of messages to log

# Create a file handler to log to a file
file_handler = logging.FileHandler('backuperV2.log')
file_handler.setLevel(logging.DEBUG)  # Set the minimum level for file logging
file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

# Create a stream handler to log to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)  # Set the minimum level for console logging
console_handler.setFormatter(file_format)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


