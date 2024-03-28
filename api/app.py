from api.PcoaFactory import PcoaFactory
from flask import Flask, render_template, request, session,send_file
import os
import uuid
from plotly.offline import plot



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
    """
    create a pcoa plot from data provided by the gnps with taskid of the user input
    Returns:
        the graph.html template with the pcoa plot if POST request
        graph.html if GET request 
    """  
    if request.method == 'POST':
        factory = PcoaFactory(session=session)
        taskId =  factory.createPcoaFromGnps(request=request)
        pcoa = f'downloads/{taskId}/index.html'
    else:
        pcoa = None
    return render_template('graph.html', pcoa=pcoa)
    
     

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
    file = None
    for key, f in request.files.items():
        print(key)
        file = f
    if file is None:
        return '', 400
    
    
    if not os.path.exists(app.config['UPLOADED_PATH']):
        os.makedirs(app.config['UPLOADED_PATH'], exist_ok=True)    

    fileId = str(uuid.uuid4())
    session['fileId'] = fileId
    file.save(os.path.join(app.config['UPLOADED_PATH'], fileId))

    return '',204


@app.route('/uploadForm', methods=['POST'])
def uploadForm():
    """
    get the file saved in the session and create a pcoa plot from it 
    
    Returns: the graph.html template with the pcoa plot if successful
    400: if the file was not found in the session
    """
    fileId = session.get('fileId')
    if fileId is None:
        return "FileId not found in session", 400
        
    file_path = os.path.join(app.config['UPLOADED_PATH'], fileId)
        
    if os.path.exists(file_path):
        pcoa = None
        with open(file_path, 'rb') as file:
            factory = PcoaFactory(session=session)
            factory.createPcoaFromFile(file,fileId)
            pcoa = f'downloads/{fileId}/index.html'    
        return render_template('graph.html', pcoa=pcoa)
    else:
         return "File not found", 404
@app.route('/usage',methods=['GET'])
def usage():
    return render_template('usage.html')    
    
if __name__=='__main__':
    #app.run(debug=True)
    app.run()

