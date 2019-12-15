FROM python:3.7-alpine

COPY . app

EXPOSE 9999

CMD ["python", "app/fdns2.py"]


