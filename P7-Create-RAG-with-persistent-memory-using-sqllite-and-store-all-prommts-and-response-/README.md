# RAG-Persistent-memory-and-web-search-using-ollama-llama3.2
download all llms from ollama locally
model="llama3.2"
model="mxbai-embed-large"
sqlite3 -- to store memory
load restaurant review data using chroma db (code shared in vector.py)


1) program - create RAG and get restaurant review file xls loaded using vector, than create persistent memory using sqllite and store all prommts and response in that.
2) Logic- search restaurant review data from loaded file, sqllite will store prompts,  search restaurant review from file then search same form from google and provide reponse on webui using streamlit.

Programs: Anyone of below can be used:
Main py - used tavily web search
Main.py - used duckduckgo_search web search


Prompt:
Create program - RAG pipeline created to load restaurant review data using chroma db (code shared in vector.py)
Create persistent memory to store prompts and responses
logic is that - we will ask for restaurant review queries which will be first looked into RAG pipeline using restaurant review data xls
Then looked into google search 
Then provide response
Webui is created using streamlit and display data

Demo code to load file is shared
Running locally using ollama (model = OllamaLLM(model="llama3.2"))
model mxbai-embed-large and llama3.2 is already loaded with ollama installed
Install required libraries
