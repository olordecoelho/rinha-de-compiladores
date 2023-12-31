
FROM python:3.11-slim-buster


RUN apt-get update && apt-get install -y


WORKDIR /var/rinha

COPY requires.txt .
RUN pip install --no-cache-dir -r requires.txt


COPY . .


CMD ["python", "indio.py"]
