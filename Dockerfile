FROM python:alpine

COPY . .

RUN pip install poetry

RUN poetry install

EXPOSE 8000
CMD poetry run fastapi run
