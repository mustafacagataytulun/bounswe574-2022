FROM python:3.8.10
ENV PYTHONUNBUFFERED 1

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ENV SECRET_KEY="changedbypipeline"
ENV DB_PASSWORD="changedbypipeline"
ENV EMAIL_HOST="changedbypipeline"
ENV EMAIL_HOST_USER="changedbypipeline"
ENV EMAIL_HOST_PASSWORD="changedbypipeline"
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

EXPOSE 8000
RUN mkdir /code
WORKDIR /code
COPY requirements_production.txt /code/
RUN pip install -r requirements_production.txt
COPY . /code/
RUN python3 manage.py collectstatic --noinput
CMD sh init.sh && python3 manage.py runserver 0.0.0.0:8000
