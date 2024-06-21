FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

RUN pip3 install torch==1.13.0+cpu torchvision==0.14.0+cpu --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip3 install Cython regex

RUN pip3 install -U openmim

RUN mim install mmcv==2.0.0rc4

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 80

# Run the application
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "80"]
