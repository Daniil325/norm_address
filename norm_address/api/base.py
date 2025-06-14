from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: str
    

class AddressResponseItem(SuccessResponse):
    result: str | None
