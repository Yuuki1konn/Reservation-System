from datetime import datetime, time
from typing import Self
from pydantic import BaseModel, ConfigDict, Field,model_validator
class ResourceCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )
    location: str = Field(
        min_length=1,
        max_length=255,
    )
    open_time: time
    close_time: time
    @model_validator(mode="after")
    def validate_business_hours(self) -> Self:
        if self.open_time >= self.close_time:
            raise ValueError("开放时间必须早于关闭时间")
        return self

class ResourceResponse(BaseModel):
    id: int
    name: str
    location: str
    open_time: time
    close_time: time
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )