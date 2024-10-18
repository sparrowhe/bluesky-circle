FROM python:3.12.7

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0" , "app:app" ]
CMD ["flask", "run", "--port=8000", "--host=0.0.0.0"]
EXPOSE 8000