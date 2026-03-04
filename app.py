from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from orchestration import RecipeGraphState, build_recipe_graph

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
    graph = build_recipe_graph()
    state = RecipeGraphState(
        user_input=f"I have {request.ingredients}",
        sanitized_input="",
        detected_allergens=request.allergies,
        retrieved_docs="",
        retrieval_score="",
        retry_count=0,
        response="",
        final_response="",
        warnings=[],
        is_safe=False,
        blocked_reason="",
        error="",
    )

    state = graph.invoke(state)
    if not state["error"]:
        return RecipeResponse(
            recipe=state["final_response"],
            warnings=state["warnings"],
            is_safe=state["is_safe"],
            error=state["error"],
        )
    return RecipeResponse(recipe="", warnings=[], is_safe=False, error=state["error"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
