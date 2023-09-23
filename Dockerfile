FROM python:3.11-alpine

WORKDIR /app

COPY ./requires.txt /files/requires.txt
COPY ./src/files/hello_world.rinha.json /files/hello_world.rinha.json
COPY . .
RUN pip install -r requires.txt

CMD ["python", "indio.py", "-r", "src/files/hello_world.rinha.json"]