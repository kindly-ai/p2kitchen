FROM python:3.10.4-slim AS builder
WORKDIR /
COPY Pipfile* /
RUN pip install pipenv==2022.1.8
RUN pipenv lock --keep-outdated -r > requirements.txt

FROM python:3.10.4-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY --from=builder /requirements.txt /app
RUN apt-get update && apt-get install git -y --no-install-recommends && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000
CMD ["gunicorn", "p2kitchen.wsgi"]
