import logging
import cloudscraper

logger = logging.getLogger(__name__)

class DiscordTicket:
    def __init__(self, proxies:dict=None):
        self.proxies = proxies
        self.session = cloudscraper.create_scraper()
        self.session.proxies = self.proxies
        self.session.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImZyLUZSIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEzMi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTMyLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3NlYXJjaC5icmF2ZS5jb20vIiwicmVmZXJyaW5nX2RvbWFpbiI6InNlYXJjaC5icmF2ZS5jb20iLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MzYzNTU3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJoYXNfY2xpZW50X21vZHMiOmZhbHNlfQ==',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'Europe/Paris',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/login',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        })
    
    def get_fingerprint(self):
        try:
            logger.info("Getting fingerprint")
            response = self.session.get("https://discord.com/api/v9/experiments")
            response.raise_for_status()
            fingerprint = response.json().get('fingerprint')
            if fingerprint is not None:
                logger.info(f"Fingerprint: {fingerprint}")
                return fingerprint
            logger.error("Error getting fingerprint")
            return None
        except Exception as e:
            logger.error(f"Error getting fingerprint: {e}")
            return None

    def exchange_ticket(self, ticket:str):
        logger.info("Exchanging ticket")
        fingerprint = self.get_fingerprint()
        if fingerprint is None:
            return None
        self.session.headers.update({
            'X-Track': fingerprint
        })
        try:
            response = self.session.post("https://discord.com/api/v9/users/@me/remote-auth/login", json={"ticket": ticket})
            if response.status_code == 400:
                logger.error("Captcha detected, did you really think I was going to give you the bypass too ? 😏🔒🤖")
                return None
            response.raise_for_status()
            encrypted_token = response.json().get('encrypted_token')
            if encrypted_token is not None:
                logger.info(f"Encrypted token: {encrypted_token}")
                return encrypted_token
            logger.error("Error exchanging ticket")
            return None
        except Exception as e:
            logger.error(f"Error exchanging ticket: {e}")
            return None