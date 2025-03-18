# 1️⃣ Use an official Python runtime as a base image
FROM python:3.9

# 2️⃣ Set the working directory inside the container
WORKDIR /app

# 3️⃣ Copy the requirements file first (for caching efficiency)
COPY requirements.txt /app/

# 4️⃣ Install dependencies (this layer gets cached if requirements.txt doesn't change)
RUN pip install -r requirements.txt

# 5️⃣ Copy the rest of the application files after installing dependencies
COPY . .  

# 6️⃣ Set permissions for all files in /app
RUN chmod -R 755 /app

# 7️⃣ Expose the API port
EXPOSE 5000

# 8️⃣ Run the application
CMD ["python3", "-u", "/app/app.py"]
