
class Database:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(cls).__new__(cls, *args, **kwargs)
            cls.__instance.ids = []
            cls.__instance.auth_tokens = {}
        return cls.__instance

    def get_token(self, chat_id):
        return self.auth_tokens[chat_id]

    def is_auth(self, chat_id):
        return chat_id in self.auth_tokens.keys()

