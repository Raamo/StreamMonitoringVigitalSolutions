FROM selenium/standalone-chromium

USER root

WORKDIR /app

COPY requirements.txt .
COPY . .


RUN pip install --upgrade pip && \
    pip install --no-cache-dir --no-warn-script-location -r requirements.txt


CMD ["python", "main.py"]
