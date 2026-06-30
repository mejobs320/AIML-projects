**# Run-ollama-locally. Create RAG locally-using-restaurant-data-to-provide-response
**

Run using ollama locally.  RAG is created in vector.py which is reading restaurant review data csv file
No need to give key as llm model="llama3.2 is downloaded locally
So program will read "restaurant review data" file and llm will answer based on that data
model = OllamaLLM(model="llama3.2")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")


Result
Run python main.py


question:
how many veg restaurant are there
LLm answer: 1 (as same data is there is restaurant file)

Note: we dont need to connect with llm using any key.
Just download olllama model and use that here (model="llama3.2" and model="mxbai-embed-large")


