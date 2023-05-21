FROM python:3.10.6

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY code .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run the command
CMD ["python", "code/main.py"]