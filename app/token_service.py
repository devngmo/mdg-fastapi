class TokenService:
    def __init__(self):
        self.tokenMap = {}
        print('TokenService::init')

    def set(self, token, metadata):
        self.tokenMap[token] = metadata

    def get(self, token):
        if token in self.tokenMap:
            return self.tokenMap[token]
        print(self.tokenMap)
        return None