FROM python:2.7

#ENV http_proxy=http://lijia.com
#ENV https_proxy=http://lijia.com
RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe"> /etc/apt/sources.list
RUN apt-get update

# Install curl
#RUN apt-get -y install vim

ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt 
CMD python app.py
