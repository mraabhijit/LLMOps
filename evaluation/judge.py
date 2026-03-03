from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from models import get_llm


def evaluate_recipe_response(query: str, context: str, response: str) -> dict:
    """Use LLM as a judge to score a recipe response."""
    judge = get_llm(provider="gemini")
    parser = JsonOutputParser()
    template = """
Judge the response on the 5 criteria:

1. Ingredient Coverage (0-10): Does the recipe use the user's ingredients?
2. Faithfulness (0-10): Is the recipe grounded in the provided context?
3. Completeness (0-10): Does it include steps, time, servings?
4. Relevance (0-10): Does the recipe match the ingredient list?
5. Safety (0-10): Are allergen warnings included when needed?

Query for the response:
{query}

Context for the response:
{context}

Response:
{response}

Return a structured response - JSON with scores and reasoning with each criterion.

"""
    prompt = ChatPromptTemplate.from_template(template=template)
    chain = prompt | judge | parser
    return chain.invoke(
        {
            "query": query,
            "context": context,
            "response": response,
        }
    )
