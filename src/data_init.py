import logging
import os

TOKEN = os.environ.get("BOT_TOKEN")
API = os.environ.get("API")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)