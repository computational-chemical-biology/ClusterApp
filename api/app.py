from flask import Flask, render_template, request, session

import os
import plotly
import json
import uuid
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import numpy as np

from gnps import Proteosafe
from utils import qiime2PCoA,filterBlank
from flask_dropzone import Dropzone

dropzone = Dropzone()
app = Flask(__name__)
app.config['DROPZONE_DEFAULT_MESSAGE'] = 'Drop Down Your Archives Here'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        taskid = uuid.uuid4()
        gnps_result = Proteosafe(request.form['taskid'], 'FBMN')
        gnps_result.get_gnps()
        if not os.path.exists(f'api/static/downloads/{taskid}'):
            os.mkdir(f'api/static/downloads/{taskid}')
        pcoa_obj = qiime2PCoA(gnps_result.meta, gnps_result.feat,
                              out_dir=f'api/static/downloads/{taskid}',
                              metric=request.form['metric'])
        pcoa = f'downloads/{taskid}/index.html'
        pcoa_file = f'api/static/downloads/{taskid}/{taskid}.qzv'
        pcoa_obj.visualization.save(pcoa_file)
        session['pcoa_file'] = f'static/downloads/{taskid}/{taskid}.qzv'
    else:
        pcoa = None

    return render_template('graph.html', pcoa=pcoa)

@app.route('/downloadplot')
def downloadplot():
    pcoa_file = session.get('pcoa_file')
    return send_file(pcoa_file, as_attachment=True)

@app.route("/upload",methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return "Invalid Archive",400

    if not file.content_type.endswith('csv'):
        return 'Send Only CSV Files',400

    try:
        dataframe = pd.read_csv(file)
        reformatedTable = filterBlank(dataframe)
        
    except Exception as e:
        return  'Fatal Error Comunicate to the Administrator: ' +str(e), 500
    
    return 'SUCESSO',200


if __name__=='__main__':
    #app.run(debug=True)
    dropzone.init_app(app)
    app.run()

