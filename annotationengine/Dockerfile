FROM python:3.10.6
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /code
COPY ./requirements_production.txt /code/requirements_production.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements_production.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
