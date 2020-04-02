#!/bin/sh
# https://docs.aws.amazon.com/de_de/elasticbeanstalk/latest/dg/single-container-docker.html
eb init -p docker --region eu-central-1
eb create covid-sim-19 

## WARNING: As of 1st april 2020, EB strips out the EXPOSE command from Dockerfile. 
## If that happens, zip this directory and upload manually in the browser!
