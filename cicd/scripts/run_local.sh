#!/bin/bash

pwd
docker stop books_app
docker rm books_app || true

docker build -t books .
docker run --name books_app -p 80:80 $(docker images -q books) 