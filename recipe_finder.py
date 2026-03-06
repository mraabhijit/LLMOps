import argparse
from pathlib import Path

import sys

from orchestration import RecipeGraphState, build_recipe_graph
from sarvam import process_voice_request_stream, process_text_request_stream


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
    if result.get("error"):
        print("\n[BLOCKED] Input rejected:")
        print(f"  {result['error']}")
        return

    # Unsafe output
    if not result.get("is_safe", True):
        print(f"\n[BLOCKED] {result.get('blocked_reason', 'Unsafe output')}")
        return

    # Warnings
    if result.get("warnings"):
        print("\n--- SAFETY WARNINGS ---")
        for w in result["warnings"]:
            print(f"  [WARNING] {w}")
        print("-----------------------")

    # Recipe
    print("\n")
    print(result.get("final_response", result.get("text", "")))


def consume_stream(stream):
    """Consume a streaming response and print to console."""
    has_printed_warnings = False
    print()
    for item in stream:
        if item.get("error"):
            print(f"\n[BLOCKED] {item['error']}")

        if item.get("is_safe") is False:
            print("\n[BLOCKED] Unsafe output")

        warnings = item.get("warnings", [])
        if warnings and not has_printed_warnings:
            print("\n--- SAFETY WARNINGS ---")
            for w in warnings:
                print(f"  [WARNING] {w}")
            print("-----------------------\n")
            has_printed_warnings = True

        text = item.get("text", "")
        if text:
            sys.stdout.write(text)
            sys.stdout.flush()
    print("\n")


def main():
    parser = argparse.ArgumentParser(description="Recipe Finder CLI")
    parser.add_argument(
        "--audio", type=str, help="Path to an audio file for Voice input."
    )
    parser.add_argument(
        "--language",
        type=str,
        default="english",
        help="Language code (e.g., english, hindi, bengali).",
    )
    parser.add_argument(
        "--text",
        type=str,
        help="Single line query of ingredients in specified language.",
    )
    args = parser.parse_args()

    if args.audio:
        print(f"\nProcessing audio file ({args.language}): {args.audio}...")
        path = Path(args.audio)
        if not path.exists():
            print("Audio file not found.")
            return
        audio_bytes = path.read_bytes()
        stream = process_voice_request_stream(audio_bytes, args.language)
        consume_stream(stream)
        return

    elif args.text:
        print(f"\nProcessing text ({args.language})...")
        if args.language.lower() == "english":
            result = run_graph(args.text)
            display_result(result)
        else:
            stream = process_text_request_stream(args.text, args.language)
            consume_stream(stream)
        return

    # Interactive flow
    query = collect_ingredients()
    if not query:
        print("No ingredients entered. Exiting.")
        return

    print("\nSearching for recipes...\n")
    if args.language.lower() == "english":
        result = run_graph(query)
        display_result(result)
    else:
        stream = process_text_request_stream(query, args.language)
        consume_stream(stream)


if __name__ == "__main__":
    main()
