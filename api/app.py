from flask import Flask, render_template, request, session, send_file

import os
import plotly
import json
import uuid
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
import numpy as np

from api.gnps import Proteosafe
from api.utils import qiime2PCoA

app = Flask(__name__)
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

if __name__=='__main__':
    #app.run(debug=True)
    app.run()

