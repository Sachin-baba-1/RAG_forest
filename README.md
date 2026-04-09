# 🌲 RAG Forest — Context-Aware Knowledge & Presentation Generator 
[Visit RAGForest](https://rag-forest.onrender.com/ui)


## 📌 Project Summary

**RAG Forest** is a context-aware document intelligence system designed to help **students, faculty, and professionals** rapidly generate:

- 📊 Context-dependent PowerPoint presentations  
- 📝 Structured notes  
- 🧩 Architecture diagrams, UML diagrams, and flowcharts  
- 📚 Comprehensive answers synthesized from multiple documents  

Unlike generic LLM-based generators, RAG Forest grounds every output **strictly in user-provided documents**, ensuring relevance, accuracy, and contextual integrity.

---
## 📑 Table of Contents

- [Project Summary](#-project-summary)
- [Goal of the Project](#-goal-of-the-project)
- [Problem Statement](#-problem-statement)
- [Target Users](#-target-users)
- [What Makes RAG Forest Different](#-what-makes-rag-forest-different)
- [Current Capabilities](#-current-capabilities-implemented)
- [Current Limitations](#-current-limitations-by-design)
- [How to Run the Project Locally](#-how-to-run-the-project-locally)
- [LLM Configuration](#-llm-configuration-current)
- [Features Under Active Development](#-features-under-active-development)
- [Future Roadmap](#-future-roadmap)
- [Platform Vision](#-platform-vision)


## 🎯 Goal of the Project

The core goal of RAG Forest is to:

> **Reduce the time and effort required to understand a topic by automatically extracting, synthesizing, and structuring knowledge from uploaded documents—while preserving user-defined context.**

This project is built around **Retrieval-Augmented Generation (RAG)** to avoid hallucinated or generic outputs and instead produce **document-faithful results**.

---

## ❓ Problem Statement

Traditional approaches to generating notes or presentations using LLMs suffer from key limitations:

- Outputs are often **generic and not context-aware**
- Documents must be **manually read and summarized**
- Diagrams and architecture flows require **separate tools**
- Information from multiple documents is **hard to consolidate**
- No grounding to **what the user actually provided**

### How RAG Forest Solves This

- Understands **user-uploaded documents**
- Allows **unlimited queries** over uploaded content
- Generates answers **only from relevant documents**
- Produces structured content suitable for:
  - PPTs
  - Notes
  - Diagrams

---

## 👥 Target Users

- 🎓 **Students** — exam preparation, concept understanding, notes  
- 👩‍🏫 **Faculty** — lecture slides, structured explanations  
- 👨‍💼 **Professionals** — architecture design, technical summaries  

---

## 🧠 What Makes RAG Forest Different

| Feature | Generic LLM Tools | RAG Forest |
|------|------------------|-----------|
| Context awareness | ❌ | ✅ |
| Multi-document synthesis | ❌ | ✅ |
| Grounded responses | ❌ | ✅ |
| Diagram-ready understanding | ❌ | ✅ |
| PPT & notes oriented | ❌ | ✅ |

---

## ✅ Current Capabilities (Implemented)

### 📄 Document Upload & Understanding
- Upload PDF documents (at least once)
- Upload multiple documents
- Text extraction from PDFs
- Documents indexed and stored for reuse

### 🔍 Querying & Retrieval
- Ask unlimited queries after upload
- Queries answered using **all relevant documents**
- Responses are **context-dependent**, not generic

### 🧩 Knowledge Synthesis
- Combines information across documents
- Produces structured, readable answers
- Designed to feed into:
  - PPT generation
  - Notes creation
  - Diagram design workflows

### 🧱 Backend Architecture
- FastAPI-based backend
- Modular RAG pipeline
- Local execution support

---

## 🚧 Current Limitations (By Design)

- Only **text content** from PDFs is processed
- Images, tables, and diagrams are **not yet interpreted**
- Manual LLM API setup required
- UI supports basic interaction (early-stage)

---

## 🚀 How to Run the Project Locally

### 🔧 Prerequisites
- Python **3.10+**
- Git
- *(Optional but recommended)* Virtual environment

---

### 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/Sachin-baba-1/RAG_forest.git
cd RAG_forest
```
### Create & Activate Virtual Environment (Optional but Recommended)
```
python -m venv env
env\Scripts\activate   # Windows
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Run the Backend
```
cd forest
fastapi dev backend/main.py
```
### Access the Application
```
http://127.0.0.1:8000/ui/
```
---
## 🔐 LLM Configuration (Current)

- Currently supports **Mistral** (manual API setup)
- User must configure the API key locally
- Selected for free and accessible experimentation

---

## 🛠️ Features Under Active Development

- 🔑 User authentication (sign-in system)
- 📂 Document selection per query
- 💬 Multiple chat sessions
- 📑 Custom number of pages for notes and PPTs
- 🎨 Template selection for presentations
- 📊 Structured PPT generation
- 📄 Exportable document notes

---

## 🔮 Future Roadmap

### 🧠 Advanced Document Understanding
- Image interpretation inside PDFs
- Table and diagram comprehension
- Context-aware diagram extraction

### 📐 Diagram & Architecture Design
- UML diagrams
- Architecture flowcharts
- Concept graphs

---

## 🌍 Platform Vision

- Hosted online platform
- No manual API setup required
- Support for multiple LLM providers
- Plug-and-play API key management
