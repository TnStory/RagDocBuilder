# Dockerfile for deploying Streamlit app with RAG Doc Builder

# Use the official Python image as a base
FROM python:3.12-bullseye

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the Streamlit server port
ENV STREAMLIT_PORT=80

# Expose the Streamlit port
EXPOSE $STREAMLIT_PORT

# Set Streamlit to run on 0.0.0.0 so it works in Fargate
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=$STREAMLIT_PORT

# Run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py"]