FROM quay.io/qiime2/amplicon:2024.5
MAINTAINER Ricardo R. da Silva <ridasilva@usp.br>

ENV INSTALL_PATH /ClusterApp
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libffi8 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
    && pip install flask gunicorn pyteomics plotly jupyter Flask-Dropzone \
       scipy scikit-bio pandas matplotlib seaborn scikit-learn \
       weasyprint==60.2 pydyf==0.10.0

COPY . .
EXPOSE 5004
CMD ["bash", "/ClusterApp/run_server.sh"]

