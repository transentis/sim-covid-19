# REST API Server for COVID-Sim

This directory contains a simple REST API server for the COVID-19 Simulation build using BPTK and Flask. The application runs standalone and does not depend on any other files outside of this directory.

The API server is currently also deployed on AWS and is used by our [COVID-19 dashboard](https://test.covid-sim.com)

## Run the COVID-19 server locally

To run the COVID-19 server locally, just run the shellscript `run_server.sh`.

Currently the server just supports one request, the /run request. This request accepts JSON structure similar to the BPTK scenario definition file as an input and responds with the relevant data.

For now we are keeping sample queries and the documentation in [Postman](https://transentis.postman.co) in the COVID-SIM API Gateway collections (use the local collection to test the server locally).

## Deploy to aws

Deploy via `eb deploy --profile development`.
