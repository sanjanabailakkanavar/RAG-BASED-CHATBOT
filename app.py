import streamlit as st
import time

from src.rag_chain import ask_question


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Software Engineering Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# SESSION STATE
# ==========================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("📚 Knowledge Base")

    st.metric("PDFs", "10")
    st.metric("Pages", "2669")
    st.metric("Chunks", "7345")

    st.success("FAISS Index Loaded")

    mode = st.selectbox(
        "🎯 Assistant Mode",
        [
            "Learning",
            "Interview",
            "Quick Revision"
        ]
    )

    st.divider()

    st.markdown("""
### 📚 Topics Covered

- Foundations of Computer Programming
- Programming in Python
- Object-Oriented Programming
- Data Structures
- Database Management Systems (DBMS)
- Operating Systems
- Computer Networks
- Information Security
- Linux & Shell Scripting
- Software Engineering
""")

    st.divider()

    if st.button("🗑️ Clear Memory"):

        st.session_state.chat_history = []

        st.rerun()

# ==========================================
# HEADER
# ==========================================

st.title("🤖 Software Engineering Knowledge Assistant")

st.info(
    "📚 Learn Concepts • 🧠 Interview Preparation • ⚡ Quick Revision"
)

if mode == "Learning":

    st.success(
        "📚 Learning Mode: Detailed explanations, examples and applications."
    )

elif mode == "Interview":

    st.success(
        "🧠 Interview Mode: Placement-focused answers, interview questions and tips."
    )

else:

    st.success(
        "⚡ Quick Revision Mode: Short notes and last-minute revision points."
    )

# ==========================================
# QUESTION INPUT
# ==========================================

question = st.text_input(
    "Ask a Question",
    placeholder="Example: Difference between Process and Thread"
)

# ==========================================
# ASK BUTTON
# ==========================================

if st.button("Ask"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        start_time = time.time()

        with st.spinner(
            "Searching documents..."
        ):

            try:

                history = "\n".join(
                    [
                        f"User: {item['question']}\nAssistant: {item['answer']}"
                        for item in st.session_state.chat_history[-3:]
                    ]
                )

                answer, sources, chunks, scores = ask_question(
                    question,
                    history,
                    mode
                )

                latency = round(
                    time.time() - start_time,
                    2
                )

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

                # ==================================
                # RESPONSE TIME
                # ==================================

                st.success(
                    f"⚡ Response Time: {latency} sec"
                )

                # ==================================
                # ANSWER
                # ==================================

                st.subheader(
                    "📘 Answer"
                )

                st.markdown(answer)

                # ==================================
                # SOURCES
                # ==================================

                st.divider()

                st.subheader(
                    "📄 Sources"
                )

                for source in sources:

                    st.write(
                        f"• {source}"
                    )

                # ==================================
                # CHUNKS
                # ==================================

                with st.expander(
                    "🔍 View Retrieved Chunks"
                ):

                    for i, chunk in enumerate(
                        chunks,
                        start=1
                    ):

                        st.markdown(
                            f"### Chunk {i}"
                        )

                        st.caption(
                            f"Similarity Score: {scores[i-1]}"
                        )

                        st.write(
                            chunk
                        )

                        st.divider()

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

# ==========================================
# CHAT HISTORY
# ==========================================

if st.session_state.chat_history:

    st.divider()

    st.subheader(
        "💬 Previous Questions"
    )

    for item in reversed(
        st.session_state.chat_history[-5:]
    ):

        with st.expander(
            item["question"]
        ):

            st.markdown(
                item["answer"]
            )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Built using LangChain • FAISS • Sentence Transformers • Groq Llama 3 • PyMuPDF • EasyOCR"
)