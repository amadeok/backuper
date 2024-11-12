
import logging

from logging.handlers import RotatingFileHandler

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  

log_file = 'backuperV2.log'
max_log_size = 5 * 1024 * 1024  # 5 MB
backup_count = 3  

rotating_handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
rotating_handler.setLevel(logging.DEBUG)
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rotating_handler.setFormatter(log_format)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(rotating_handler)
logger.addHandler(console_handler)