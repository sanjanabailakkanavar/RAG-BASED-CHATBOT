# 🤖 Software Engineering Knowledge Assistant

## Overview

Software Engineering Knowledge Assistant is an AI-powered Retrieval-Augmented Generation (RAG) chatbot designed to help students learn software engineering concepts, prepare for technical interviews, and revise important topics for placement examinations.

The system retrieves information from a private knowledge base consisting of multiple software engineering PDFs and generates accurate, context-aware answers using Large Language Models (LLMs).

Unlike traditional chatbots, the assistant provides answers directly from trusted study materials and includes source references for better reliability and transparency.

---

## Problem Statement

Students preparing for placements often need to study from multiple subjects such as:

- Operating Systems
- Database Management Systems (DBMS)
- Computer Networks
- Data Structures
- Programming in Python
- Object-Oriented Programming
- Linux
- Information Security
- Software Engineering

Searching through hundreds or thousands of pages to find specific information can be time-consuming.

This project solves that problem by allowing students to ask questions in natural language and receive instant answers from the study material.

---

## How It Helps Students

### 📚 Learning Mode

Provides detailed explanations of concepts similar to a teacher.

Students can:
- Understand concepts from basics
- Learn working principles
- Study examples
- Explore applications and real-world use cases
- Revise related topics

Example Questions:

- What is Python?
- Explain Deadlock in Operating Systems.
- What is Normalization in DBMS?

---

### 🧠 Interview Mode

Designed specifically for placement preparation.

Students can:
- Learn interview-focused definitions
- Practice frequently asked interview questions
- Prepare concise answers
- Understand common mistakes
- Revise key interview points

Example Questions:

- Difference between Process and Thread
- Explain TCP vs UDP
- What are ACID Properties?

---

### ⚡ Quick Revision Mode

Provides short and concise notes for last-minute revision.

Students can:
- Revise important concepts quickly
- Review key points before interviews
- Memorize important technical keywords
- Prepare for aptitude and technical rounds

---

## Key Features

- Retrieval-Augmented Generation (RAG)
- Semantic Search using FAISS
- Source Citation Support
- Learning Mode
- Interview Preparation Mode
- Quick Revision Mode
- Conversation Memory
- OCR Support for Scanned PDFs
- Fast Response Time (typically 1–3 seconds)
- Open-Source Embedding Model

---

## Knowledge Base

The chatbot is trained on study materials covering:

1. Foundations of Computer Programming
2. Programming in Python
3. Object-Oriented Programming
4. Data Structures
5. Database Management Systems (DBMS)
6. Operating Systems
7. Computer Networks
8. Information Security
9. Linux & Shell Scripting
10. Software Engineering

Total Knowledge Base:

- 10 PDFs
- 2669+ Pages
- 7345+ Chunks

---

## Technology Stack

### Frontend

- Streamlit

### Backend

- Python

### Retrieval Layer

- LangChain
- FAISS Vector Database

### Embedding Model

- Sentence Transformers
- all-MiniLM-L6-v2

### Large Language Model

- Groq Llama 3.1 8B Instant

### Document Processing

- PyMuPDF
- EasyOCR

---

## Benefits for Placement Preparation

This assistant acts as a personal study companion by helping students:

- Learn concepts faster
- Revise multiple subjects efficiently
- Prepare for technical interviews
- Practice interview questions
- Reduce time spent searching through study materials
- Access information from thousands of pages instantly

The system is especially useful for final-year students preparing for campus placements, internships, technical interviews, and competitive examinations.