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
        user_input = input()
        if user_input.lower() in ["exit", "quit"]:
            break
        ingredients.append(user_input.lower())

    ingredients_str = ", ".join(ingredients)
    print(f"\nSearching for recipes with: {ingredients_str}\n\n")

    query = "I have " + ingredients_str
    print(chain.invoke(query, config={"callbacks": [get_langfuse_handler()]}))


if __name__ == "__main__":
    main()
