import json
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from pipeline import run_pipeline
from routers.auth import get_current_user
from sarvam import process_voice_request_stream, process_text_request_stream


class RecipeRequest(BaseModel):
    ingredients: str
    allergies: list[str] = []
    language: str = "english"


class RecipeResponse(BaseModel):
    recipe: str
    warnings: list[str] = []
    is_safe: bool
    error: Optional[str] = None


router = APIRouter()


@router.post("/recipe", response_model=RecipeResponse)
def get_recipe(request: RecipeRequest, current_user: str = Depends(get_current_user)):
    response = run_pipeline(
        english_input=request.ingredients, allergies=request.allergies
    )
    return RecipeResponse(
        recipe=response["recipe"],
        warnings=response["warnings"],
        is_safe=response["is_safe"],
        error=response["error"],
    )


@router.post("/recipe/voice")
def get_recipe_from_voice(
    audio: UploadFile = File(...),
    language: str = Form("english"),
    current_user: str = Depends(get_current_user),
):
    audio_bytes = audio.file.read()

    def generator():
        for chunk in process_voice_request_stream(audio_bytes, language):
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")


@router.post("/recipe/text")
def get_recipe_from_text(
    request: RecipeRequest, current_user: str = Depends(get_current_user)
):
    def generator():
        for chunk in process_text_request_stream(request.ingredients, request.language):
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")
