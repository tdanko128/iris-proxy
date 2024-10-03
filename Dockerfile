# iris_proxy Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the application files
COPY app.py .
COPY config.json .
COPY custom_modules/ custom_modules/

# Copy requirements and install them
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
