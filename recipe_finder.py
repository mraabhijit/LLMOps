from orchestration import RecipeGraphState, build_recipe_graph


def collect_ingredients() -> str:
    """Collect ingredients from user via CLI input."""
    ingredients = []
    print("Welcome to Recipe Finder")
    print("=========================")
    print(
        "Enter available ingredients, each ingredient in a new line.\n"
        "You can also mention allergies (e.g., 'allergic to dairy').\n"
        "Type 'quit' or 'exit' when done.\n"
    )
    while True:
        user_input = input("> ")
        if user_input.lower().strip() in ["exit", "quit"]:
            break
        if user_input.strip():
            ingredients.append(user_input.lower().strip())

    if not ingredients:
        return ""

    return "I have " + ", ".join(ingredients)


def run_graph(query: str) -> dict:
    """Build and invoke the LangGraph recipe pipeline."""
    graph = build_recipe_graph()
    state = RecipeGraphState(
        user_input=query,
        sanitized_input="",
        detected_allergens=[],
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
    return graph.invoke(state)


def display_result(result: dict):
    """Format and display the graph result to the console."""
    # Error / blocked input
    if result["error"]:
        print("\n[BLOCKED] Input rejected:")
        print(f"  {result['error']}")
        return

    # Unsafe output
    if not result["is_safe"]:
        print(f"\n[BLOCKED] {result['blocked_reason']}")
        return

    # Warnings
    if result["warnings"]:
        print("\n--- SAFETY WARNINGS ---")
        for w in result["warnings"]:
            print(f"  [WARNING] {w}")
        print("-----------------------")

    # Recipe
    print("\n")
    print(result["final_response"])


def main():
    query = collect_ingredients()
    if not query:
        print("No ingredients entered. Exiting.")
        return

    print("\nSearching for recipes...\n")
    result = run_graph(query)
    display_result(result)


if __name__ == "__main__":
    main()
