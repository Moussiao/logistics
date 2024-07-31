from ninja import Schema


class TokenRequest(Schema):
    tma_init_data: str


class TokenResponse(Schema):
    token: str
