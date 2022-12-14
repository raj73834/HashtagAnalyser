FROM python:3.7

# ENV PYTHONUNBUFFERED 1

WORKDIR /app

# COPY . /app

ADD . /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip 

# RUN pip install wordcloud
RUN pip install -r requirements.txt

COPY . .