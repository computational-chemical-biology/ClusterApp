import traceback
from flask import Flask, jsonify,  redirect, render_template, request, session,send_file, url_for
from api.src.controller.csv_from_gnps_controller import CsvFromGnpsController
from api.src.controller.dropzone_upload_handler import DropzoneUploadHandler
from api.src.controller.graph_controller import GraphController
from api.src.controller.upload_edited_csv_controller import UploadEditedCsvController
from api.src.service.pcoa_from_file_service import PcoaFromFileService
from api.src.utils.GnpsRequestException import GnpsRequestException
from api.src.utils.utils import createFile, getFile

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOADED_PATH'] = '/ClusterApp/api/static/downloads'

@app.route('/graph', methods=['GET', 'POST'])
def graph():  
    try:
        controller = GraphController(request,session,app)
        return controller.executeGraph()
    except GnpsRequestException as e:
        return e, 500
    except Exception as e:
        stack_trace = traceback.format_exc()
        return jsonify({'error': 'An internal error occurred', 'details': str(e), 'trace': stack_trace}), 500
    
@app.route('/downloadplot')
def downloadplot():
    """
        download the pcoa plot file
        Returns: the pcoa plot file 
    """
    pcoa_file = session.get('pcoa_file')
    return send_file(pcoa_file, as_attachment=True)

@app.route('/dropzoneUploadHandler', methods=['POST'])
def dropzoneUploadHandler():
    try:
        controller = DropzoneUploadHandler(request,session,app,PcoaFromFileService(session=session))
        return controller.executeDropzoneUpload()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/usage',methods=['GET'])
def usage():
    return render_template('usage.html')    

@app.route('/mountDataTable', methods=['POST','GET'])
def mountDataTable():
    """
    create a file from the user input and return dataTable.html template
    Returns: the dataTable.html template
    """
    createFile(request,session,app)
    return render_template('dataTable.html')


@app.route('/download_csv', methods=['GET'])
def download_csv():
    """
        used to send data to the dataTable.html template
        Returns: the csv file
    """
    file = getFile(session,app)
    if file is None:
        return "File not found", 404
    
    return send_file(file, as_attachment=True)
    

@app.route('/uploadEditedCsv', methods=['POST','GET'])
def uploadEditedCsv():
    try:
        controller = UploadEditedCsvController(request,session,app,PcoaFromFileService(session=session))
        return jsonify({'pcoa':controller.executeUploadEditedCsv()})
    except Exception as e:
        return 'internal server error',500
    
@app.route('/render_graph')
def render_graph():
    pcoa = request.args.get('pcoa')
    return render_template('graph.html', pcoa=pcoa)

@app.route('/csv_from_gnps', methods=['POST'])
def csv_from_gnps():
    """
    create a csv file from the gnps user task
    Returns: the csv file
    """
    controller = CsvFromGnpsController(request=request,session=session,app=app)
    csv_path = controller.get_csv_from_gnps()
    return send_file(
        csv_path,
        mimetype='text/csv',
        as_attachment=True, 
        download_name='output.csv'
    )

@app.route('/data_gathering', methods=['GET'])
def data_gathering():
    return render_template('dataGathering.html')
     

@app.route('/error')
def error():
    error = request.args.get('error')
    return render_template('error.html', error=error)

@app.errorhandler(500)
def error(error):
    return render_template('error.html', error=error)


if __name__=='__main__':
    #app.run(debug=True)
    app.run()

