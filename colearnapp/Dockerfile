FROM python:3.8.10
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
COPY requirements_production.txt /code/
RUN pip install -r requirements_production.txt
COPY . /code/
RUN python3 manage.py collectstatic --noinput
CMD sh init.sh && python3 manage.py runserver 0.0.0.0:8000
