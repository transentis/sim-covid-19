FROM python:3
ADD sim-covid-19_dashboard_only.ipynb /
ADD src /src/
RUN mkdir /simulation_models
RUN mkdir /scenarios/
RUN pip install voila bptk_py ipywidgets
RUN jupyter nbextension enable --py widgetsnbextension

EXPOSE 80

CMD ["voila","sim-covid-19_dashboard_only.ipynb","--no-browser","--port=80"]
