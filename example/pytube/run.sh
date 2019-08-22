docker build -t webget .
docker rm webget
docker run -it --name webget webget
