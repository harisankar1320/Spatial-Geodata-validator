# base Python image
FROM python:3.11-slim

# set working directory inside container
WORKDIR /app

# copy requirements first (for faster builds)
COPY requirements.txt .

# install all libraries
RUN pip install --no-cache-dir -r requirements.txt

# copy all your code
COPY src/ ./src/

# expose the port Streamlit runs on
EXPOSE 8501

# command to run the app
CMD ["streamlit", "run", "src/web_app.py", "--server.port=8501", "--server.address=0.0.0.0"]