FROM python:3.6

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1


# Creation of the workdir
RUN mkdir /code

WORKDIR /code

# Add requirements.txt file to container
ADD requirements.txt /code/

# Install requirements
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt

# Add the current directory(the web folder) to Docker container
ADD . /code/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver","0.0.0.0:8000"]

# commands
## sudo docker build -t capstone18_project .
## sudo docker run -p 8000:8000 capstone18_project
## ngrok http 8000