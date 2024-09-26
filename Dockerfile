FROM quay.io/qiime2/core:2023.7
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /ClusterApp
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

#for production
RUN pip install flask gunicorn pyteomics plotly jupyter Flask-Dropzone
#for testing
#RUN pip install flask gunicorn pyteomics plotly jupyter Flask-Dropzone pytest

COPY . .
EXPOSE 5004
CMD ["bash", "/ClusterApp/run_server.sh"]

#CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "api.app:app"

