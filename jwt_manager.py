from jwt import encode, decode

@staticmethod
def create_token(data: dict) -> str:
    token : str = encode(
                        payload=data
                        ,key="mysecretkey"
                        ,algorithm="HS256"
                        )
    return token

@staticmethod
def validate_token(token: str) -> dict:
    data: dict = decode(token, key="mysecretkey", algorithms=['HS256'])
    return data