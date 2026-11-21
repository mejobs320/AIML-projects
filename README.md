All Projects Explained  

Project 1: Multimodal Image Recognition & Visual Q&A Web App
This project gives you a web page where you can upload an image, see what is inside it, and ask follow-up questions about what you see.   
**What it does**: You open the app in your browser, pick an image file (such as a photo of a Golden Retriever holding a flower), and click to analyze it. The app returns a main subject, a list of other visible objects, and a short description of the scene. Afterward, you can type follow-up questions about the same image, such as asking about the colors of the dog and the flower.   
**How it works behind the scenes**: Python and Streamlit run the web interface and keep track of your session. The uploaded image is handled with Pillow and encoded in base64 so it can be sent with a structured prompt to a vision-language model on the Groq API (such as Qwen3.8-27B, which can be updated through a configuration setting).   

Project 2: Hybrid RAG Restaurant Review Assistant with Persistent Memory
This project is a chatbot web app that answers questions about restaurant reviews from a CSV file and also checks the web when helpful, while saving your chat history

**What it does**: You type a question in the Streamlit web page (or click a quick question). The app searches the restaurant review data from realistic_restaurant_reviews.csv (including overall review stats like counts, ratings, and dates) and also pulls live web search results. It combines that information to give an answer, shows where the answer came from, and displays your past questions and answers in the interface.

**How it works behind the scenes**: A vector setup script loads realistic_restaurant_reviews.csv into a persistent ChromaDB index using Sentence-Transformers embeddings (all-MiniLM-L6-v2) so the app can find similar reviews. A separate SQLite database stores every question, answer, source, and timestamp. When you ask a question, LangChain and the Groq model (openai/gpt-oss-120b) use the retrieved reviews and web search results (via DuckDuckGo, with Tavily also noted) to write the response.   

Project 3: Custom MCP Server for Local RAG, SQLite Analytics & Live Web Search
This project connects your restaurant review data, search tools, and web search to an AI assistant like Claude Desktop using the Model Context Protocol (MCP).   
**What it does**: Instead of only using a standalone Streamlit chat page, this project exposes seven tools through an MCP server so a compatible client like Claude Desktop can look up reviews, check review statistics, filter by star rating, search by keyword, check conversation history, or run web searches. For example, you can ask Claude to show 5-star reviews or answer general web questions using the connected tools. It also includes a test script (test_mcp.py) that runs all seven functions directly to verify they work.   
**How it works behind the scenes**: The MCP server (mcp_server.py) runs in Python and can connect locally using stdio (such as with Claude Desktop) or over HTTP using Server-Sent Events (SSE) with Starlette and Uvicorn. It uses Ollama locally for language generation (Llama 3.2) and embeddings (mxbai-embed-large), LangChain and ChromaDB for vector search, SQLite for structured review data and chat history, Pandas for CSV processing, and the Tavily API for live web search.   
