# create-programs-for-image-recognition-and-load-in-docker-file
Image recognition program loaded into docker file. So now it can run in any environment.

one with groq llm  (used llm - Llama Vision)  Model:** `llama-3.2-11b-vision`            ----- main.py  with streamlit
streamlit run main.py  -- ui will open -- share image


Share with others:
Option 1: Save as a file (No internet needed)
On your computer — save image to a file:
powershelldocker save -o ai-image-classifier.tar ai-image-classifier

This creates a ai-image-classifier.tar file — share it via USB/Google Drive/etc.
On the other computer — load and run:
powershelldocker load -i ai-image-classifier.tar
docker run -p 8501:8501 ai-image-classifier
