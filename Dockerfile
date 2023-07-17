# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run the Python script
CMD ["python", "dandok_news.py"]
