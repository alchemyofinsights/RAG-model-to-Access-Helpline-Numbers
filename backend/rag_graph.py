from typing import TypedDict, List
from langgraph.graph import StateGraph
from vector_store import retrieve_helplines_rag
from hf_llm import llm  # if you want advice via LLM

# ---------- STATE ----------
class HelplineState(TypedDict):
    age: int
    state: str
    scenario: str
    helplines: List[dict]
    advice: str

# ---------- NODES ----------
# ---------- NODES ----------

# Replace your old SQL/database node with this
def rag_retrieval_node(state: HelplineState) -> HelplineState:
    """Retrieve helplines from FAISS vector store, national first, then state-specific."""
    retrieved = retrieve_helplines_rag(
        age=state["age"],
        state=state["state"],
        scenario=state["scenario"],
        top_k=5
    )
    state["helplines"] = retrieved
    return state

from langchain_core.messages import SystemMessage, HumanMessage

def advice_node(state: HelplineState) -> HelplineState:
    """Generate short advice using chat LLM, grounded in retrieved helplines."""

    if not state["helplines"]:
        state["advice"] = (
            "I couldn’t find a specific helpline for this situation. "
            "If you feel unsafe right now, please contact local emergency services."
        )
        return state

    helpline_text = "\n".join(
        f"- {h['helpline_name']} ({h['phone_number']}): {h['description']}"
        for h in state["helplines"]
    )

    messages = [
        SystemMessage(
            content=(
                "You are a calm, supportive safety assistant. "
                "You must only use the helplines provided. "
                "Do not invent resources. Do not diagnose. "
                "Keep advice short, reassuring, and practical."
            )
        ),
        HumanMessage(
            content=(
                f"User situation:\n{state['scenario']}\n\n"
                f"Available helplines:\n{helpline_text}\n\n"
                "Give brief, emotionally supportive guidance."
            )
        )
    ]

    response = llm.invoke(messages)
    
    # advice_text = response.content

    # # 🔹 Remove chat-style prefixes if present
    # if "[ASSISTANT]" in advice_text:
    #     advice_text = advice_text.split("[ASSISTANT]", 1)[-1].strip()

    # if "[USER]" in advice_text:
    #     advice_text = advice_text.split("[USER]", 1)[0].strip()

    import re

    advice_text = response.content
    advice_text = re.sub(r"\[USER\].*?\n", "", advice_text, flags=re.DOTALL)
    advice_text = re.sub(r"\[ASSISTANT\]\s*", "", advice_text)

    state["advice"] = advice_text.strip()

    # state["advice"] = ad
    return state
# ---------- GRAPH ----------
graph = StateGraph(HelplineState)

graph.add_node("rag_retrieval", rag_retrieval_node)
graph.add_node("advice", advice_node)

graph.set_entry_point("rag_retrieval")
graph.add_edge("rag_retrieval", "advice")

# Compile for Flask
app_graph = graph.compile()