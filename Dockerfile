FROM python:3
ADD sim-covid-19.ipynb /
ADD images /images/
RUN pip install voila bptk_py
CMD ["voila","sim-covid-19.ipynb","--no-browser","--port=80"]
