# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port Streamlit will run on (Cloud Run uses 8080 by default)
EXPOSE 8080

# Command to run the app with settings for Cloud Run
CMD ["streamlit", "run", "vigil_agent.py", "--server.port=8080", "--server.address=0.0.0.0"]