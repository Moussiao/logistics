from ninja import Schema


class ErrorEntity(Schema):
    msg: str
    type: str
    field: str | None = None
    loc: list[str] | None = None
    ctx: dict[str, str] | None = None


class ErrorResponse(Schema):
    detail: list[ErrorEntity]
