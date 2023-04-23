FROM python:3.11.3-bullseye
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install Django==4.2
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
EXPOSE 3000
