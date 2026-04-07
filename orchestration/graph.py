from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from guardrails import InputRail, InputRailResponse, OutputRail, OutputRailResponse
from pipeline.generator import format_docs, load_prompt
from pipeline.retriever import get_retriever
from tracing import get_langfuse_handler


class RecipeGraphState(TypedDict):
    user_input: str
    sanitized_input: str
    detected_allergens: list[str]
    retrieved_docs: str
    retrieval_score: str
    retry_count: int
    response: str
    final_response: str
    warnings: list[str]
    is_safe: bool
    blocked_reason: str
    error: str


def input_guard(state: RecipeGraphState) -> RecipeGraphState:
    input_rail = InputRail()
    response: InputRailResponse = input_rail.check_input(state["user_input"])
    if not response.is_valid:
        state["error"] = " ".join(response.violations)
        return state

    state["sanitized_input"] = response.sanitized_input
    state["detected_allergens"] = response.detected_allergens
    return state


async def retrieve(state: RecipeGraphState) -> RecipeGraphState:
    retriever = get_retriever()
    docs = await retriever.ainvoke(state["sanitized_input"])
    docs_str = format_docs(docs)
    state["retrieved_docs"] = docs_str
    return state


def evaluate_retrieval(state: RecipeGraphState) -> RecipeGraphState:
    if len(state["retrieved_docs"]) < 50:
        state["retrieval_score"] = "bad"
        state["retry_count"] += 1
        state["retry_count"] = min(2, state["retry_count"])
        return state

    state["retrieval_score"] = "good"
    return state


async def generate(state: RecipeGraphState) -> RecipeGraphState:
    from pipeline import batcher
    
    prompt = load_prompt()

    rendered_prompt = prompt.format(
        context=state["retrieved_docs"],
        question=state["sanitized_input"],
    )

    state["response"] = await batcher.add_request(rendered_prompt)
    return state


def output_guard(state: RecipeGraphState) -> RecipeGraphState:
    output_rail = OutputRail()
    response: OutputRailResponse = output_rail.check_output(
        response=state["response"],
        user_defined_allergen=state["detected_allergens"],
    )

    state["final_response"] = response.response
    state["warnings"] = response.warnings
    state["is_safe"] = response.is_safe
    state["blocked_reason"] = response.blocked_reason
    return state


def route_after_input_guard(state: RecipeGraphState) -> str:
    if state["error"]:
        return END
    return "retrieve"


def route_after_evaluation(state: RecipeGraphState) -> str:
    if state["retrieval_score"] == "bad" and state["retry_count"] < 2:
        return "retrieve"
    return "generate"


def build_recipe_graph():
    graph = StateGraph(state_schema=RecipeGraphState)

    graph.add_node("input_guard", input_guard)
    graph.add_node("retrieve", retrieve)
    graph.add_node("evaluate_retrieval", evaluate_retrieval)
    graph.add_node("generate", generate)
    graph.add_node("output_guard", output_guard)

    graph.add_edge(START, "input_guard")
    graph.add_conditional_edges(
        "input_guard",
        route_after_input_guard,
        {
            "retrieve": "retrieve",
            END: END,
        },
    )
    graph.add_edge("retrieve", "evaluate_retrieval")
    graph.add_conditional_edges(
        "evaluate_retrieval",
        route_after_evaluation,
        {
            "retrieve": "retrieve",
            "generate": "generate",
        },
    )
    graph.add_edge("generate", "output_guard")
    graph.add_edge("output_guard", END)

    return graph.compile()
