FROM python:3.9-slim

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask API code
COPY . .

# Expose the port that your Flask API listens to
EXPOSE 5000

# Specify the command to start the Flask API
CMD ["python", "app.py"]
