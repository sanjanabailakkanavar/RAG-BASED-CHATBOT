import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# CONFIG
# ==========================================

VECTORSTORE_PATH = "vectorstore"


# ==========================================
# EMBEDDING MODEL
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# LOAD FAISS INDEX
# ==========================================

vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)


# ==========================================
# GROQ LLM
# ==========================================

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


# ==========================================
# RAG FUNCTION
# ==========================================

def ask_question(query, history="", mode="Learning"):

    # ======================================
    # RETRIEVE DOCUMENTS + SCORES
    # ======================================

    results = vectorstore.similarity_search_with_score(
        query,
        k=7
    )

    docs = [
        doc
        for doc, score in results
    ]

    scores = [
        round(float(score), 4)
        for doc, score in results
    ]

    # ======================================
    # BUILD CONTEXT
    # ======================================

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    # ======================================
    # LEARNING MODE
    # ======================================

    if mode == "Learning":

        prompt = f"""
You are an expert Software Engineering Professor and Technical Trainer.

Previous Conversation:
{history}

Use ONLY the information available in the context.

If the answer is not present in the context, reply:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{query}

Teach the topic like a professor.

Format the answer as:

# Topic Name

## What is it?

## Why is it Needed?

## Detailed Explanation

## How it Works

## Key Features

## Types / Components (If Applicable)

## Syntax / Structure (If Applicable)

## Example

## Advantages

## Disadvantages

## Applications

## Real World Example

## Common Mistakes

## Related Topics

## Quick Revision Notes

## Practice Questions

Use markdown formatting.

Highlight important technical terms using **bold**.
"""

    # ======================================
    # INTERVIEW MODE
    # ======================================

    elif mode == "Interview":

        prompt = f"""
You are an expert Technical Interviewer and Placement Trainer.

Previous Conversation:
{history}

Use ONLY the information available in the context.

If the answer is not present in the context, reply:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{query}

Generate an interview-focused answer.

Format the answer as:

# Topic Name

## Interview Definition

## 30-Second Answer

## Key Interview Points

## Comparison Table (If Applicable)

## Most Asked Interview Questions

## Sample Answers

## Expected Follow-Up Questions

## Common Mistakes

## Company-Oriented Questions

## Interview Tip

## Quick Revision

Use markdown formatting.

Highlight important technical terms using **bold**.
"""

    # ======================================
    # QUICK REVISION MODE
    # ======================================

    else:

        prompt = f"""
You are an expert Software Engineering Revision Assistant.

Previous Conversation:
{history}

Use ONLY the information available in the context.

If the answer is not present in the context, reply:
"I could not find the answer in the provided documents."

Context:
{context}

Question:
{query}

Generate concise revision notes.

Format:

# Topic Name

## Definition

## Key Points

## Important Features

## Interview Keywords

## Common Questions

## 1-Minute Revision Notes

Keep the answer short and easy to revise.

Use markdown formatting.

Highlight important technical terms using **bold**.
"""

    # ======================================
    # GENERATE ANSWER
    # ======================================

    response = llm.invoke(
        prompt
    )

    # ======================================
    # SOURCES
    # ======================================

    sources = []

    for doc in docs:

        filename = doc.metadata.get(
            "filename",
            "Unknown File"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        sources.append(
            f"{filename} (Page {page})"
        )

    # ======================================
    # RETRIEVED CHUNKS
    # ======================================

    chunks = []

    for doc in docs:

        chunks.append(
            doc.page_content[:1000]
        )

    # ======================================
    # RETURN
    # ======================================

    return (
        response.content,
        list(set(sources)),
        chunks,
        scores
    )