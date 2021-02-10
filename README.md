# COVID-19 Simulation

This repository contains a simulation of the COVID-19 pandemic based on the SIR model. The simulation is currently roughly calibrated to the situation in Germany and illustrates some scenarios regarding social distancing, with the objective of keeping the strain on the health care system at a tolerable level.

You can play with the simulation and the scenarios using Jupyter notebooks, the simulation itself is built using System Dynamics as implemented in the [BPTK-Py](http://bptk.transentis-labs.com) simulation framework.

The simulation includes a dashboard that can be run interactively in Jupyter or as a standalone application using [Voila](https://voila.readthedocs.io). You can see the dashboard in action on [covid-sim.com](https://covid-sim.com)

## Repository Contents

Currently the repository contains two versions of the SIR model, one built using the System Dynamics DSL implemented in BPTK-Py and one in XMILE format, built using the System Dynamics modeling environment [Stella Architect](http://www.iseesystems.com)

We have included a notebook for each:

* [COVID-19 Simulation](sim-covid-19.ipynb) The notebook contains the complete simulation written in Python, nothing else needed.
* [COVID-19 Simulation (XMILE)](sim-covid-19-xmile.ipynb) The underlying simulation was created in XMILE using Stella Architect, but the Jupyter notebook is fully functional even if you don't have a Stella Architect license. The Stella Architect file is in `simulation_models/sir_model.stmx`



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
4. Activate the virtual environment: ```source venv/bin/activate``` (MacOS/Linux) or ```venv\scripts\activate.bat``` (Windows)
5. Install the necessary python modules: ```pip install -r requirements.txt```
7. Install Jupyter widgets (for the interactive dashboard): ```jupyter labextension install @jupyter-widgets/jupyterlab-manager```
8. Start JupyerLab: ```jupyter lab```
9. Your browser will open showing JupyterLab and your chosen directory
10. Open the notebook ```sim-covid-19.ipynb``` from within JupyterLab and run all cells.

## Running the dashboard using Voila

Next to the full Jupyter notebook we have also included a stripped down version that only includes the interactive dashboard. You can run the dashboard locally using [Voila](https://voila.readthedocs.io/en/stable/). Follow  these steps:

1. Install voila:    ```pip install voila```
2. Run the dashboard: ```voila sim-covid-19_dashboard_only.ipynb```

This will run the dashboard and open it in your browser.

## Deploying the dashboard via AWS Elastic Beanstalk

If you have Amazon Web Services at your disposal, you can deploy the dashboard on AWS Elastic Beanstalk with a single click, including auto-scaling groups and fault tolerance.

- ``awscli``: [https://docs.aws.amazon.com/de_de/cli/latest/userguide/cli-chap-install.html](https://docs.aws.amazon.com/de_de/cli/latest/userguide/cli-chap-install.html)
- ``ebcli``: [https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)


The deploy script only uses two commands:

```bash
eb init -p docker --region eu-central-1
eb create covid-sim-19
```

You can update an application using

```bash
eb init covid-sim-19 --region eu-central-1
eb deploy
```

### Local testing

For __local testing__, run:

```bash
eb init -p docker --region eu-central-1
eb local run --port 8001
```

This will start the application on your local machine on port 8001. Access via [http://localhost:8001](http://localhost:8001)

## Get In Touch

Please let us know if you need help getting started, if you find a bug or are missing important functionality.

You can best reach us per e-mail at [support@transentis.com](mailto:support@transentis.com)
