# Use a lightweight Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files
COPY . .

# Copy entrypoint script explicitly
COPY entrypoint.sh /entrypoint.sh

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint executable
RUN chmod +x /entrypoint.sh

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
CMD ["cli"]
