from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing_extensions import Self

class ReservationCreate(BaseModel):
    resource_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime
    @field_validator(
        "start_time",
        "end_time",
    )
    @classmethod
    def validate_timezone(cls, value: datetime,) -> datetime:
        if value.utcoffset() is not None:
            raise ValueError("当前版本请使用不带时区后缀的北京时间")
        return value
    
    @model_validator(mode="after")
    def validate_time_range(self) -> Self:
        if self.start_time >= self.end_time:
            raise ValueError("预约开始时间必须早于结束时间")
        return self

class ReservationResponse(BaseModel):
    id: int
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: str
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
    )