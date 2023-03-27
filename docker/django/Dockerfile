FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app/django
COPY requirements*.txt ./
RUN pip install -r requirements.txt -r requirements.scrapy.txt -r requirements.debug.txt
RUN python -m spacy download en_core_web_md
COPY . .
EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
