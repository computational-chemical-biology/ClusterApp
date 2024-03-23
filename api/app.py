from api.PcoaFactory import PcoaFactory
from flask import Flask, render_template, request, session,send_file, redirect, url_for
import traceback

import os
import plotly
import json
import uuid
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import numpy as np

from api.gnps import Proteosafe
from api.utils import makePcoa, qiime2PCoA
from flask_dropzone import Dropzone

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(os.getcwd(), 'api/static/downloads'),
    DROPZONE_DEFAULT_MESSAGE = 'Drop Down Your Archives Here',
    DROPZONE_MAX_FILES=1,
    DROPZONE_UPLOAD_ACTION='uploadArchive', 
    DROPZONE_AUTO_PROCESS_QUEUE=False,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_BTN_ID='submit'
)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
dropzone = Dropzone(app)

@app.route('/graph', methods=['GET', 'POST'])
def graph():    
    if request.method == 'POST':
        factory = PcoaFactory(session=session)
        pcoa = factory.getPcoaFromGnps(request=request)
    else:
        pcoa = None
    return render_template('graph.html', pcoa=pcoa)
    
     

@app.route('/downloadplot')
def downloadplot():
    pcoa_file = session.get('pcoa_file')
    return send_file(pcoa_file, as_attachment=True)


@app.route('/uploadArchive', methods=['GET', 'POST'])
def uploadArchive():
    file = None
    for key, f in request.files.items():
        file = f

    if not os.path.exists(app.config['UPLOADED_PATH']):
        os.makedirs(app.config['UPLOADED_PATH'], exist_ok=True)    

    fileId = str(uuid.uuid4())
    session['fileId'] = fileId
    file.save(os.path.join(app.config['UPLOADED_PATH'], fileId))

    return '',204


@app.route('/uploadForm', methods=['POST'])
def uploadForm():
    fileName = session.get('fileId')
    file_path = os.path.join(app.config['UPLOADED_PATH'], fileName)
     
    if os.path.exists(file_path):
        pcoa = None
        with open(file_path, 'rb') as file:
            factory = PcoaFactory(session=session)
            pcoa = factory.getPcoaFromFile(file)    
        return render_template('graph.html', pcoa=pcoa)
    else:
        return "File not found", 404
    
if __name__=='__main__':
    #app.run(debug=True)
    app.run()

