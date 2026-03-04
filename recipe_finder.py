from guardrails import InputRail, OutputRail
from pipeline import create_rag_chain
from tracing import get_langfuse_handler


def main():
    chain = create_rag_chain()
    ingredients = []
    print("Welcome to Recipe Finder")
    print("=========================")
    print(
        "Enter available ingredients, each ingredient in a new line. To exit or end, type exit or quit."
    )
    while True:
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        ingredients.append(user_input.lower())

    ingredients_str = ", ".join(ingredients)
    query = "I have " + ingredients_str

    input_rail = InputRail()
    input_rail_output = input_rail.check_input(query)
    print(f"\nInput Check: {'Passed' if input_rail_output['is_valid'] else 'FAILED'}")
    if not input_rail_output["is_valid"]:
        print("\nInput rejected:")
        for v in input_rail_output["violations"]:
            print(f"  - {v}")
        return
    if input_rail_output["detected_allergens"]:
        allergens = ", ".join(input_rail_output["detected_allergens"])
        print(f"  [ALLERGY NOTED] {allergens}")

    print(f"\nSearching for recipes with: {ingredients_str}\n\n")

    response = chain.invoke(query, config={"callbacks": [get_langfuse_handler()]})

    output_rail = OutputRail()
    output_rail_result = output_rail.check_output(
        response, input_rail_output["detected_allergens"]
    )

    if not output_rail_result["is_safe"]:
        print(f"\n[BLOCKED] {output_rail_result['blocked_reason']}")
        return

    # Print warnings first
    if output_rail_result["warnings"]:
        print("\n--- SAFETY WARNINGS ---")
        for w in output_rail_result["warnings"]:
            print(f"  [WARNING] {w}")
        print("-----------------------")

    # Print the response (which already has allergen banners prepended by OutputRail)
    print("\n")
    print(output_rail_result["response"])


if __name__ == "__main__":
    main()
