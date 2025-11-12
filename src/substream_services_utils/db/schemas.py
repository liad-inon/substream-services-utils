from datetime import datetime

from pydantic import BaseModel, NonNegativeFloat


class UserData(BaseModel):
    transcriptionMinutesLeft: NonNegativeFloat
    userName: str
    email: str
    subscriptionType: str
    paddleCustomerId: str


class TranscriptionJobProgress(BaseModel):
    statusMessage: str
    isSuccess: bool
    isFailure: bool
    expireAt: datetime
