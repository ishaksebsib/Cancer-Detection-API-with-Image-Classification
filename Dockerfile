# Pull base image
FROM python:3.10.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies for cv2
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install TensorFlow
RUN pip install tensorflow==2.9.1

# Install OpenCV python
RUN pip install opencv-python==4.8.0.74



# Install Python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .
