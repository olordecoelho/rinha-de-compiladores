FROM python:3.11-alpine

WORKDIR /app

COPY ./requires.txt /app/requires.txt
COPY ./var/rinha/ /var/rinha/
COPY . .
RUN pip install -r requires.txt

CMD ["python", "indio.py", "-r", "/var/rinha/fib.rinha.json"]