import json
from pathlib import Path

from langchain_text_splitters.character import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE


def _load_recipes(file_path: Path | str = Path("data/recipes.json")) -> list[dict]:
    """Load and return recipes from the JSON file."""
    try:
        with open(file_path, "r") as f_in:
            recipes = json.load(f_in)
            return recipes
    except FileNotFoundError as e:
        raise FileNotFoundError(e)


def _recipe_to_text(recipe: dict) -> str:
    """Convert a single recipe dict into a flat text string for embedding."""
    return (
        f"Recipe Name: {recipe.get('name', '')}\n"
        f"Cuisine: {recipe.get('cuisine', '')}\n"
        f"Dietary Metadata: {recipe.get('dietary', [])}\n"
        f"Allergens: {recipe.get('allergens', [])}\n"
        f"Prep Time (mins): {recipe.get('prep_time_mins', 10)}\n"
        f"Cooking Time (mins): {recipe.get('cook_time_mins', 10)}\n"
        f"Servings: {recipe.get('servings', 2)}\n"
        f"Difficulty: {recipe.get('difficulty', '')}\n"
        f"Ingredients: {_get_ingredients(recipe.get('ingredients', []))}\n"
        f"Instructions: {_get_instructions(recipe.get('instructions', []))}\n"
        f"Tips: {recipe.get('tips', '')}."
    )


def get_recipe_chunks(file_path: Path | str = Path("data/recipes.json")):
    """Load recipes, convert to text, split into chunks, return Documents."""
    recipes = _load_recipes(file_path)
    recipes_list = [_recipe_to_text(recipe) for recipe in recipes]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )
    return text_splitter.create_documents(recipes_list)


def _get_ingredients(ingredients: list[dict]) -> str:
    """Returns the ingredients in a flat structure."""
    return ", ".join(
        f"{ing['quantity']} {ing['unit']} of {ing['item']}" for ing in ingredients
    )


def _get_instructions(instructions: list[str]) -> str:
    """Returns the instructions in a flat structure."""
    return " ".join(f"Step {i + 1}: {step}" for i, step in enumerate(instructions))


if __name__ == "__main__":
    print(get_recipe_chunks()[:2])
