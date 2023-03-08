#!/bin/sh
docker cp $(docker ps -aqf "name=jamco"):/backend/static/ ./static/
aws s3 rm --recursive  s3://jamco/static/
aws s3 sync ./static/  s3://jamco/static/
