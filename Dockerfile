FROM python:3.12
WORKDIR /usr/local/app

# Copy the application dependencies list
COPY requirements.txt ./

# Create saves file, sets up app user, and adds needed permissions
RUN mkdir ./saves && useradd app && chown app ./saves

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
WORKDIR ./src

USER app

ENV PYTHONPATH /usr/local/app
CMD ["python3", "main.py"]