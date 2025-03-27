from langgraph.graph import StateGraph, MessagesState, START, END
from tts_stt_backend import text_to_speech_omeife, speech_to_text_omeife

# Build the state graph
graph = StateGraph(MessagesState)

# Text-to-Speech Node
def tts_node(state: MessagesState):
    text = state["messages"][-1]["content"]
    language = state.get("language", "en")
    persona = state.get("persona", "male")
    audio_file = text_to_speech_omeife(text, language, persona)

    state["messages"].append({"role": "assistant", "audio": audio_file})
    return state

# Speech-to-Text Node
def stt_node(state: MessagesState):
    audio_path = state["audio_path"]
    language = state.get("language", "en")
    transcript = speech_to_text_omeife(audio_path, language)

    state["messages"].append({"role": "assistant", "content": transcript})
    return state

# Add nodes to the graph
graph.add_node("tts", tts_node)
graph.add_node("stt", stt_node)
graph.add_edge(START, "tts")
graph.add_edge("tts", "stt")
graph.add_edge("stt", END)
