FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
COPY setup.py .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy the rest of the application
COPY . .

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Set up environment
ENV PYTHONUNBUFFERED=1

# Default command
ENTRYPOINT ["materials_aggregator"]
CMD ["--help"]

# Usage instructions in the container
LABEL maintainer="John Wroge <wrogejohn@gmail.com>"
LABEL description="Materials Research Aggregator for chemists"
LABEL usage="docker run -e MATERIALS_PROJECT_API_KEY='your_key' materials-aggregator search Li,O"