import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

class DiscordCrypto:
    def __init__(self):
        self.key = RSA.generate(2048)
        self.cipher = PKCS1_OAEP.new(self.key, hashAlgo=SHA256)

    def decrypt(self, data):
        return self.cipher.decrypt(data)

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def get_proof(self, nonce):
        return base64.urlsafe_b64encode(SHA256.new(data=self.decrypt(base64.b64decode(nonce))).digest()).decode().rstrip('=')

    def get_proof_b64(self, nonce):
        return self.get_proof(nonce).b64encode()

    def decrypt_payloads(self, encrypted_payload):
        return self.decrypt(base64.b64decode(encrypted_payload)).decode()
    @property
    def public_key(self):
        pub_key = self.key.publickey().export_key().decode('utf-8')
        pub_key = ''.join(pub_key.split('\n')[1:-1])
        return pub_key