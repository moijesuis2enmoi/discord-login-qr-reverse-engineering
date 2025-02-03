

class User:
    def __init__(self, **values):
        self.id = values.get('id')
        self.username = values.get('username')
        self.discrim = values.get('discrim')
        self.avatar_hash = values.get('avatar_hash')
        self.token = values.get('token')

    @classmethod
    def from_payload(cls, payload):
        values = payload.split(':')

        return cls(id=values[0],
                   discrim=values[1],
                   avatar_hash=values[2],
                   username=values[3])

    @property
    def __str__(self):
        return f"DiscordUser(id={self.id}, username={self.username}, discrim={self.discrim}, avatar_hash={self.avatar_hash}, token={self.token})"

    @property
    def __dict__(self):
        return {
            'id': self.id,
            'username': self.username,
            'discrim': self.discrim,
            'avatar_hash': self.avatar_hash,
            'token': self.token
        }