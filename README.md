# COVID-19 Simulation

This repository contains a simulation of the COVID-19 pandemic based on the SIR model. The simulation is currently roughly calibrated to the situation in Germany and illustrates some scenarios regarding social distancing, with the objective of keeping the strain on the health care system at a tolerable level.

You can play with the simulation and the scenarios using Jupyter notebooks, the simulation itself is built using System Dynamics as implemented in the BPTK-Py simulation framework.

You can read more about BPTK-Py in the [BPTK-Py online documentation](http://bptk.transentis-labs.com).

## Installation

### Using Docker

If you have Docker installed (e.g. Docker Desktop on MacOS or on Windows), follow these steps:

1. On the command line, move into a directory where you would like to store the COVID-19 repository. 
2. Clone this repository: ```git clone https://github.com/transentis/sim-covid-19.git```
3. Run ```docker-compose up```
4. Point your browser at [http://localhost:8888](http://localhost:8888) – this will open JupyterLab showing the contents of your directory. 
5. Open the notebook ```sim-covid-19.ipynb``` from within JupyterLab and run all cells.
6. When you are finished, close your browser and call ```docker-compose down``` from within your directory. This will stop and remove the container.

### Using a virtual environment

First, make sure you have Python 3 installed on your machine.

Then follow these steps:

1. On the command line, move into a directory where you would like to store the COVID-19 repository. 
2. Clone this repository: ```git clone https://github.com/transentis/sim-covid-19.git```
3. Install a virtual environment in that directory: ```python3 -m venv venv```
4. Activate the virtual environment: ```source venv/bin/activate``` (MacOS/Linux) or ``venv\scripts\activate.bat``` (Windows)
5. Install the necessary python modules: ```pip install -r requirements.txt```
7. Install Jupyter widgets (for the interactive dashboard): ```jupyter labextension install @jupyter-widgets/jupyterlab-manager```
8. Start JupyerLab: ```jupyter lab```
9. Your browser will open showing JupyterLab and your chosen directory
10. Open the notebook ```sim-covid-19.ipynb``` from within JupyterLab and run all cells.

## Contents

Currently the repository contains two versions of the SIR model, one built using the System Dynamics DSL implemented in BPTK-Py and one in XMILE format, built using the System Dynamics modeling environment [Stella Architect](http://www.iseesystems.com)`

We have included a notebook for each - the notebooks produce identical results.

* [COVID-19 Simulation](sim-covid-19.ipynb) The notebook contains the complete simulation written in Python.
* [COVID-19 Simulation (XMILE)](sim-covid-19-xmile.ipynb) The simulation was created in XMILE using Stella Architect, but the notebook is fully functional even if you don't have a Stella Architect license. The Stella Architect file is in `simulation_models/sir_model.stmx`

## Get In Touch

Please let us know if you need help getting started, if you find a bug or are missing important functionality.

You can best reach us per e-mail at [support@transentis.com](mailto:support@transentis.com)
