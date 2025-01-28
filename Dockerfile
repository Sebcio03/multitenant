FROM python:3.12

WORKDIR /usr/src/app

RUN apt-get update -y && apt-get upgrade -y

RUN pip install poetry==1.6.1
COPY src/poetry.lock src/pyproject.toml ./
RUN poetry install

COPY src .

ENTRYPOINT ["poetry", "run","python", "manage.py", "runserver", "0.0.0.0:8000"]