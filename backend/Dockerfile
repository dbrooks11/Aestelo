# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (to cache dependencies)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run Flask globally on 0.0.0.0 so Docker can see it
# --debug enables hot reloading
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]