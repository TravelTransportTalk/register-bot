import logging
import os

TOKEN = os.environ.get("BOT_TOKEN")
API = os.environ.get("API")
WEBUI_BASE_URL = os.environ.get("WEBUI_BASE_URL")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)