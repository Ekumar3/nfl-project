# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for caching efficiency)
COPY requirements.txt /app/

# Install dependencies (this layer gets cached if requirements.txt doesn't change)
RUN pip install -r requirements.txt

# Copy the rest of the application files after installing dependencies
COPY . .  

# Set permissions for all files in /app
RUN chmod -R 755 /app

# Expose the API port
EXPOSE 5000

# Run the application
CMD ["python3", "-u", "/app/app.py"]
