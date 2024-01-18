# Use official Python runtime as a parent image
FROM python:3.11.7

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install core dependencies
RUN python -m pip install --upgrade pip

RUN apt-get update && apt-get install -y pkg-config libpango1.0-dev

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available
EXPOSE 80

# Define environment variable
ENV NAME World

# Run the app when the container launches
CMD ["python", "app.py"]
