from orchestration import RecipeGraphState, build_recipe_graph


def run_pipeline(english_input: str, allergies: list[str]) -> dict:
    graph = build_recipe_graph()
    state = RecipeGraphState(
        user_input=english_input,
        sanitized_input="",
        detected_allergens=allergies,
        retrieved_docs="",
        retrieval_score="",
        retry_count=0,
        response="",
        final_response="",
        is_safe=False,
        blocked_reason="",
        error="",
        warnings=[],
    )

    state = graph.invoke(state)

    if state["error"]:
        return {
            "recipe": "",
            "is_safe": False,
            "error": state["error"],
            "warnings": state["warnings"],
        }

    return {
        "recipe": state["final_response"],
        "is_safe": state["is_safe"],
        "error": state["error"],
        "warnings": state["warnings"],
    }
