# Use the official Python image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV PYTHONPATH=/app

# Command to run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "3000"]
