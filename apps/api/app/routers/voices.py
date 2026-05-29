from fastapi import APIRouter

from app.schemas import VoiceRead

router = APIRouter(tags=["voices"])


@router.get("/voices", response_model=list[VoiceRead])
def list_voices() -> list[VoiceRead]:
  return [
    VoiceRead(id="mimo_default", name="mimo_default"),
    VoiceRead(id="mimo-mia", name="Mia"),
    VoiceRead(id="mimo-chloe", name="Chloe"),
    VoiceRead(id="mimo-milo", name="Milo"),
    VoiceRead(id="mimo-dean", name="Dean"),
  ]
