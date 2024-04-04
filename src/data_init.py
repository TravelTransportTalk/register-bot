import logging
import os

TOKEN = os.environ.get("BOT_TOKEN")
API = os.environ.get("API")
WEBUI_BASE_URL = os.environ.get("WEBUI_BASE_URL")
WEBHOOK_PUBLIC_URL = os.environ.get("WEBHOOK_PUBLIC_URL")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET")
WEBHOOK_BIND_HOST = os.environ.get("WEBHOOK_BIND_HOST", "0.0.0.0")
WEBHOOK_BIND_PORT = os.environ.get("WEBHOOK_BIND_PORT", "8080")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
