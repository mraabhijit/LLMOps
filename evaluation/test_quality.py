from evaluation.judge import evaluate_recipe_response
from pipeline.generator import create_rag_chain, format_docs
from pipeline.retriever import get_retriever

TEST_CASES = [
    # Partial match — user has some ingredients but missing key ones
    {"query": "I have garlic and olive oil", "expected": "Multiple partial matches"},
    # No match — ingredients not in any recipe
    {
        "query": "I have lobster, saffron, truffle oil, asparagus",
        "expected": "No good match",
    },
    # Ambiguous — these ingredients match 5+ recipes
    {
        "query": "I have garlic, tomato, onion",
        "expected": "Ambiguous - multiple recipes",
    },
    # Allergen trap — user mentions an allergy, pipeline should catch it
    {
        "query": "I have peanuts, eggplant, sesame seeds. I am allergic to peanuts",
        "expected": "Bagara Baingan with allergy warning",
    },
    # Cross-cuisine confusion — ingredients that span different cuisines
    {
        "query": "I have rice, coconut milk, soy sauce, garam masala",
        "expected": "Unclear match",
    },
]


def run_evaluation(test_cases: list[dict] = TEST_CASES) -> list[dict]:
    """Run test cases through the RAG pipeline and evaluate quality."""
    chain = create_rag_chain()
    retriever = get_retriever()
    results = []

    for i, test in enumerate(test_cases):
        print(f"\n--- Test Case {i}/{len(test_cases)} ---")
        print(f"Query: {test['query']}")
        print(f"Expected: {test['expected']}")

        context_docs = retriever.invoke(test["query"])
        context_str = format_docs(context_docs)
        response = chain.invoke(test["query"])

        scores = evaluate_recipe_response(
            query=test["query"],
            context=context_str,
            response=response,
        )

        result = {
            "query": test["query"],
            "expected": test["expected"],
            "response": response,
            "scores": scores,
        }
        results.append(result)
        print(f"Scores: {scores}")

    print("\n\n=== EVALUATION SUMMARY ===")
    for r in results:
        print(f"\nQuery: {r['query']}")
        print(f"Expected: {r['expected']}")
        print(f"Scores: {r['scores']}")

    return results


if __name__ == "__main__":
    run_evaluation()
