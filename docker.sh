docker build . -t yaml

docker run --rm -it --name yaml yaml

docker exec -it yaml /bin/bash