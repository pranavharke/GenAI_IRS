
# 🤖 GenAI-IRS: Intelligent Document Question Answering System

A powerful, LLM-backed information retrieval system built using **LangChain**, **FAISS**, and **Streamlit**. GenAI-IRS enables users to upload and interact with PDF documents using natural language queries. With semantic search and metadata-aware responses, it delivers contextually accurate answers that are traceable to their sources.


## 🚀 Key Features

- 📄 **Multi-PDF Upload**: Upload and process multiple PDF documents via an intuitive sidebar.
- 🔍 **Semantic Search Engine**: Uses FAISS to chunk and embed text for rapid, vector-based retrieval.
- 🧠 **LLM-Driven Answers**: Backed by **GROQ’s `llama3-70b-8192`**, delivering high-quality, structured responses.
- 💬 **Context-Persistent Conversations**: Maintains memory using `ConversationBufferMemory` for coherent dialogue.
- 🧾 **Source Attribution**: Answers include document source references for transparency and verification.
- 🖥️ **Minimalist UI**: Clean, responsive Streamlit interface for seamless interaction.


## 📁 Project/File Structure

```
GenAI-IRS/
├── app.py                   # Streamlit app entry point
├── .env                     # API keys and configuration (excluded from version control)
├── .gitignore               # Files/directories to ignore in git
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── setup.py                 # Python packaging config
├── src/
    ├── __init__.py          # Package initialization
    └── helper.py            # Core utilities: text parsing, embedding, chains
```

## ⚙️ Installation Guide

### 1. Clone the repository
```bash
git clone https://github.com/pranavharke/GenAI_IRS.git
cd GenAI_IRS
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a `.env` file in the root directory with:
```bash
GROQ_API_KEY="YOUR_API_KEY_HERE"
```

## 🧪 Running the App

```bash
> streamlit run app.py
```
- It may automatically redirect to following website [http://localhost:8501](http://localhost:8501) in your browser (or paste in browser)

### Usage Instructions:
- Upload one or more PDF files from the sidebar.
- Click **Submit** to extract and index the content.
- Use the chat box to ask questions about your documents.
- Receive well-structured answers sourced from your uploaded PDFs.

## 🧱 Built With

| Component                 | Role                                        |
|--------------------------|---------------------------------------------|
| Python                   | Core Programming language                               |
| Streamlit                | WebApplication framework                            |
| pdfplumber               | PDF content extraction                      |
| FAISS                    | Efficient vector search                     |
| LangChain                | Conversational logic, chaining, and memory  |
| GROQ (llama3-70b-8192)   | Large Language Model backend                |
| HuggingFace Embeddings   | Text vector encoding                        |
| python-dotenv            | Environment variable handling               |


## 📄 License

This project is licensed under the MIT License

```bash
MIT License

Copyright ©️ Pranav Harke

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
```
---

### Crafted with Curiosity 🤔 & Fueled by Tea ☕
