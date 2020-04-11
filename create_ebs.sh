#!/bin/sh
# https://docs.aws.amazon.com/de_de/elasticbeanstalk/latest/dg/single-container-docker.html
eb init -p docker --region eu-central-1
eb create covid-sim-19 

