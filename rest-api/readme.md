# REST API Server for COVID-Sim

This directory contains a simple REST API server for the COVID-19 Simulation build using BPTK and Flask. The application runs standalone and does not depend on any other files outside of this directory.

The API server is currently also deployed on AWS and is used by our [COVID-19 dashboard](https://test.covid-sim.com)

## Run the COVID-19 server locally

Please note this requires at least Python 3.8  

Follow these steps to install and run this server locally

1) git clone https://github.com/transentis/sim-covid-19 

2) Create a virtual environment and activate it: “source <your venv>/bin/activate”  

3) cd sim-covid-19 && cd rest-api

4) pip3 install -r requirements.txt  

5) ./run_server.sh 

6) You can test this at the url: localhost:5000 which should return a screen “BPTK Simulation Service”

Currently the server just supports one request, the /run request. This request accepts JSON structure similar to the BPTK scenario definition file as an input and responds with the relevant data.

For now we are keeping sample queries and the documentation in [Postman](https://transentis.postman.co) in the COVID-SIM API Gateway collections (use the local collection to test the server locally).

## Deploy to aws

Deploy via `eb deploy --profile development`.
