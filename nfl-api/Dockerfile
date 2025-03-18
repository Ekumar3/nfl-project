# Use Python runtime as base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY . .

# Expose the API port
EXPOSE 5000

# Run the Application
CMD ["python", "app.py"]

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
