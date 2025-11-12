from datetime import datetime

from pydantic import BaseModel, NonNegativeFloat

# --- COLLECTION KEYS ---
USER_DATA_COLLECTION = "userData"
TRANSCRIPTION_JOB_PROGRESS_COLLECTION = "subtitlesCreationJobProgres"

# --- userData FIELDS ---
TRANSCRIPTION_MINUTES_LEFT_FIELD = "transcriptionMinutesLeft"
USER_NAME_FIELD = "userName"
SUBSCRIPTION_TYPE_FIELD = "subscriptionType"

# --- subtitlesCreationStatus FIELDS ---
STATUS_MESSAGE_FIELD = "statusMessage"


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
