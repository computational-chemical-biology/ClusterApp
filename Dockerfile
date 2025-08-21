FROM quay.io/qiime2/core:2023.7
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /ClusterApp
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

# Instala dependências do sistema necessárias para o WeasyPrint
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi7 \
    && rm -rf /var/lib/apt/lists/*

#for production
RUN pip install --upgrade pip \
    && pip install flask gunicorn pyteomics plotly jupyter Flask-Dropzone \
       scipy scikit-bio pandas matplotlib seaborn scikit-learn \
       weasyprint==60.2 pydyf==0.10.0
#for testing
#RUN pip install flask gunicorn pyteomics plotly jupyter Flask-Dropzone pytest

COPY . .
EXPOSE 5004
CMD ["bash", "/ClusterApp/run_server.sh"]

#CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "api.app:app"

