FROM python:3.8
ADD sim-covid-19_dashboard_only.ipynb /
ADD src /src/
RUN mkdir /simulation_models
RUN mkdir /scenarios/
RUN pip install voila bptk_py ipywidgets
RUN jupyter nbextension enable --py widgetsnbextension

EXPOSE 80

CMD ["voila","--no-browser","--port=80","--MappingKernelManager.cull_interval=30","--MappingKernelManager.cull_idle_timeout=150","sim-covid-19_dashboard_only.ipynb"]
