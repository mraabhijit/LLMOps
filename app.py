from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from pipeline import run_pipeline

app = FastAPI()


class RecipeRequest(BaseModel):
    ingredients: str
    allergies: list[str] = []


class RecipeResponse(BaseModel):
    recipe: str
    warnings: list[str] = []
    is_safe: bool
    error: Optional[str] = None


@app.post("/recipe", response_model=RecipeResponse)
def get_recipe(request: RecipeRequest):
    response = run_pipeline(
        english_input=request.ingredients, allergies=request.allergies
    )
    return RecipeResponse(
        recipe=response["recipe"],
        warnings=response["warnings"],
        is_safe=response["is_safe"],
        error=response["error"],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
