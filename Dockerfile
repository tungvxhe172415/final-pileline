FROM python:3.7
EXPOSE 5012
WORKDIR /pythonProjectRBAC
ADD . /pythonProjectRBAC
RUN pip install -r requirements.txt
CMD gunicorn --workers=3 --threads=1 --timeout=3600 --preload -b 0.0.0.0:5012 server:app