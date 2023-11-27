from datetime import datetime
from loguru import logger

current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_name = f"{current_datetime}.log"
logger.add(f"./logs/{log_file_name}", rotation="500 MB", level="TRACE")
