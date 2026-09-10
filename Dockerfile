FROM python:3.10-slim
WORKDIR /usr/local/app

# Install application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . ./

EXPOSE 8080

# Setup an app user so container doesn't run as root
RUN useradd -m app && chown -R app:app /usr/local/app
USER app

CMD ["uvicorn", "APP.main:app", "--host", "0.0.0.0", "--port", "8080"]