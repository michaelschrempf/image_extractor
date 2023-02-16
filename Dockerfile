FROM python:3.8

# Install required system packages
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages
RUN pip install Pillow pytesseract flask

# Expose port 5000 for Flask app
EXPOSE 5000

ENV FLASK_APP=main

# Start the Flask app
CMD ["flask", "run" ,"--host=0.0.0.0"]