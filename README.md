# COVID-19 Simulation

This repository contains a simulation of the COVID-19 pandemic based on the SIR model. The simulation is roughly calibrated to the situation as it was in Germany in March 2020. It illustrates some scenarios regarding social distancing, with the objective of keeping the strain on the health care system at a tolerable level.

The main objective of the simulation is to illustrate how to use the BPTK-Py simulation framework. 
You can play with the simulation and the scenarios using Jupyter notebooks, the simulation itself is built using System Dynamics as implemented in the [BPTK-Py](http://bptk.transentis-labs.com) simulation framework.

The simulation also includes a dashboard that can be run interactively in Jupyter or as a standalone application using [Voila](https://voila.readthedocs.io). 

There is a companion repository on [Github](https://github.com/transentis/sim-covid-dashboard) that illustrates how to build a web-based dashboard that runs against a REST-API provided by the COVID simulation.  You can take a look at a live version of the dashboard at [www.covid-sim.com](http://www.covid-sim.com), you can find instructions how to start the REST-API server down below.

## Repository Contents

Currently the repository contains two versions of the SIR model, one built using the System Dynamics DSL implemented in BPTK-Py and one in XMILE format, built using the System Dynamics modeling environment [Stella Architect](http://www.iseesystems.com)

We have included a notebook for each:

* [COVID-19 Simulation](sim-covid-19.ipynb) The notebook contains the complete simulation written in Python, nothing else needed.
* [COVID-19 Simulation (XMILE)](sim-covid-19-xmile.ipynb) The underlying simulation was created in XMILE using Stella Architect, but the Jupyter notebook is fully functional even if you don't have a Stella Architect license. The Stella Architect file is in `simulation_models/sir_model.stmx`

The repository also contains a REST-API server, which you can find in the [rest-api](./rest-api) folder.

## Installation

### Using Docker

If you have Docker installed (e.g. Docker Desktop on MacOS or on Windows), follow these steps:

1. On the command line, move into a directory where you would like to store the COVID-19 repository. 
2. Clone this repository: `git clone https://github.com/transentis/sim-covid-19.git`
3. Run `docker-compose up`
4. Point your browser at [http://localhost:8888](http://localhost:8888) – this will open JupyterLab showing the contents of your directory. 
5. Open the notebook `sim-covid-19.ipynb` from within JupyterLab and run all cells.
6. When you are finished, close your browser and call `docker-compose down` from within your directory. This will stop and remove the container.

### Using a virtual environment

First, make sure you have Python 3 installed on your machine.

Then follow these steps:

1. On the command line, move into a directory where you would like to store the COVID-19 repository. 
2. Clone this repository: `git clone https://github.com/transentis/sim-covid-19.git`
3. Install a virtual environment in that directory: `python3 -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate` (MacOS/Linux) or `venv\scripts\activate.bat` (Windows)
5. Install the necessary python modules: `pip install -r requirements.txt`
7. Install Jupyter widgets (needed for the interactive dashboard): `jupyter labextension install @jupyter-widgets/jupyterlab-manager`
8. Start JupyerLab: `jupyter lab`
9. Your browser will open showing JupyterLab and your chosen directory
10. Open the notebook `sim-covid-19.ipynb` from within JupyterLab and run all cells.

## Running the Jupyter dashboard using Voila

Next to the full Jupyter notebook we have also included a stripped down version that only includes the interactive dashboard. You can run the dashboard locally using [Voila](https://voila.readthedocs.io/en/stable/). Follow  these steps:

1. Install voila:    `pip install voila`
2. Run the dashboard: `voila sim-covid-19_dashboard_only.ipynb`

This will run the dashboard and open it in your browser.

## Running the REST-API server

The repository includes a REST-API server that enables access to the COVID-Simulation via a REST-API. There is a companion repository on [Github](https://github.com/transentis/sim-covid-dashboard) that illustrates how to build a web-based dashboard that runs against that REST-API.  You can take a look at a live version of the dashboard at [www.covid-sim.com](http://www.covid-sim.com).

To run the server, please follow these steps:

1. Start the venv in the root directory (if you haven't done so yet): `source venv/bin/activate`
2. Switch in to the rest-api directory: `cd rest-api`
3. Make the run-script runnable: `chmod +x run_server.sh`
4. Start the server using the script: `./run_server.sh`

The server should now be running on port 5000, you can test it by calling  [http://localhost:5000](http://localhost:5000) in the browser. This should show a simple message to indicate that the server is running.

You can also test the  REST api on the command line via curl: A call to `curl localhost:5000/scenarios` will deliver the set of scenarios known to the server, this should look much like the following:

```
[
  "smSir_base",
  "smSir_dashboard",
  "smSir_avoid_the_peak",
  "smSir_strong_social_distancing",
  "smSir_weak_social_distancing"
]
```

There is also a Jupyter notebook [api_tests.ipynb](./rest-api/api_tests.ipynb) in the rest-api directory that illustrates some more advanced queries.

## Get In Touch

Please let us know if you need help getting started, if you find a bug or are missing important functionality.

You can best reach us per e-mail at [support@transentis.com](mailto:support@transentis.com)
