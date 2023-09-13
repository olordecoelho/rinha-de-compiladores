FROM python:3.9

WORKDIR /app

COPY src ./
COPY ./src/files/fib.rinha.json /src/files/fib.rinha.json
COPY requirements.txt ./

CMD ["python", "main.py", "-s", "/src/files/fib.rinha.json"]