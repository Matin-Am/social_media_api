FROM python:latest 

RUN mkdir /app 
WORKDIR /app 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip 
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt 

COPY ./django_social /app/

EXPOSE 8000 

