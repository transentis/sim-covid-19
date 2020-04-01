FROM python:3
ADD sim-covid-19.ipynb /
ADD images /images/
ADD src /src/
RUN mkdir /simulation_models
RUN mkdir /scenarios/
RUN pip install voila bptk_py ipywidgets matplotlib jupyterlab
RUN jupyter nbextension enable --py widgetsnbextension
#RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager

EXPOSE 80

CMD ["voila","sim-covid-19.ipynb","--no-browser","--port=80"]
