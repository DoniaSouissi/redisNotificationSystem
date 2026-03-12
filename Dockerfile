# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 5000 for the Flask web server
EXPOSE 5000

# Command to run the Flask application
# (Assuming your app.py is in the root directory or webVersion folder. 
CMD ["python", "webVersion/app.py"]