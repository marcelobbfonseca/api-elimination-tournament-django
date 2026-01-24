FROM python:3.11.3-bullseye
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

# install dependencies for pyaudio. required for vapi.
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt /code/
RUN pip install Django==4.2
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
EXPOSE 3000
