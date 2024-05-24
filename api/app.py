from flask import Flask,  redirect, render_template, request, session,send_file, url_for
import os
from api.src.controller.csv_from_gnps_controller import CsvFromGnpsController
from api.src.controller.graph_controller import GraphController
from api.src.controller.upload_edited_csv_controller import UploadEditedCsvController
from api.src.controller.upload_form_controller import UploadFormController
from api.src.service.pcoa_from_file_service import PcoaFromFileService
from api.src.utils.utils import createFile, getFile
from flask_dropzone import Dropzone

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(os.getcwd(), 'api/static/downloads'),
    DROPZONE_DEFAULT_MESSAGE = 'Drop Down Your Archives Here To Generate The PCoA Plot',
    DROPZONE_MAX_FILE_SIZE = 25,
    DROPZONE_MAX_FILES=1,
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE = '.csv',
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
    controller = GraphController(request,session,app)
    return controller.executeGraph()
    
@app.route('/downloadplot')
def downloadplot():
    """
        download the pcoa plot file
        Returns: the pcoa plot file 
    """
    pcoa_file = session.get('pcoa_file')
    return send_file(pcoa_file, as_attachment=True)


@app.route('/uploadArchive', methods=['GET', 'POST'])
def uploadArchive():
    """
    upload an file to the server and save it in the UPLOADED_PATH and save the fileId in the session to be used later
    Returns: 
        204: if the file was uploaded successfully
        400: if the file was not provided by the user 
    """
    createFile(request=request,session=session,app=app)
    return '',204


@app.route('/uploadForm', methods=['POST'])
def uploadForm():
    """
    get the file saved in the session and create a pcoa plot from it 
    
    Returns: the graph.html template with the pcoa plot if successful
    400: if the file was not found in the session
    """
    try:
        controller = UploadFormController(request,session,app,PcoaFromFileService(session=session))
        return controller.executeUploadForm()
    except Exception as e:
        return redirect(url_for('error', error=e))
    

@app.route('/usage',methods=['GET'])
def usage():
    """
        Returns: the usage.html template
    """
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
        return controller.executeUploadEditedCsv()
    except Exception as e:
        return redirect(url_for('error', error=e))
    
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
     

@app.route('/error')
def error():
    error = request.args.get('error')
    return render_template('error.html', error=error)

@app.errorhandler(500)
def error(error):
    return render_template('error.html', error=error)

@app.errorhandler(400)
def badRequest():
    return render_template('error.html', error='Bad Request')

if __name__=='__main__':
    #app.run(debug=True)
    app.run()

