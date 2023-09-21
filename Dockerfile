FROM quay.io/qiime2/core:2023.7
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /ClusterApp
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN pip install flask gunicorn pyteomics plotly

COPY . .
#CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "api.app:app"

