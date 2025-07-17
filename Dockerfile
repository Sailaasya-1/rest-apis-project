#Trying to run gunicorn
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
#RUN pip install flask
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]

# Before depolying into the render
# FROM python:3.10
# EXPOSE 5000 
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# RUN pip install flask
# COPY . .
# CMD ["flask", "run", "--host" , "0.0.0.0"]