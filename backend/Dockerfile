FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

# Install necessary packages and clean up cache
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Copy the application code
COPY . /app

# Run the application with a delay to wait for dependencies to be ready
CMD sleep 30s && python app.py --host 0.0.0.0 --port 5000
