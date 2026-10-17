FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set the working directory (this automatically creates /app)
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files into the working directory
COPY app.py test_app.py ./

# Now change ownership of the /app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
