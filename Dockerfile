FROM python:3.12
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create saves file
RUN mkdir ./saves

# Copy in the source code
COPY src ./src
WORKDIR ./src

# Setup an app user so the container doesn't run as the root user
RUN useradd app
RUN chown app ../saves
USER app

ENV PYTHONPATH /usr/local/app
CMD ["python3", "main.py"]