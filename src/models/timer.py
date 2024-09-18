from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional


class SetTimerRequest(BaseModel):
    """Validation model for  set timer request"""
    hours: Optional[int] = Field(0, ge=0)  
    minutes: Optional[int] = Field(0, ge=0)  
    seconds: Optional[int] = Field(0, ge=0) 
    url: HttpUrl  # Validate that it's a valid URL


class SetTimerResponse(BaseModel):
    """Validation model for set timer response."""
    id: str
    time_left: int

    # Configure Pydantic to allow arbitrary types
    model_config = ConfigDict(arbitrary_types_allowed=True)


class GetTimerResponse(BaseModel):
    """Validation model for set timer response."""
    id: str
    time_left: int

    # Configure Pydantic to allow arbitrary types
    model_config = ConfigDict(arbitrary_types_allowed=True)
