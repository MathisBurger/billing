from flask import Flask, flash, redirect, request, send_from_directory, url_for
from main import default_runner
import os
import subprocess

UPLOAD_FOLDER = "./upload"
ALLOWED_EXTENSIONS = {'pdf'}
WANTED_FILES = ["ABRG", "Anschreiben", "BWA", "BEW", "EGT"]

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.add_url_rule(
    "/process/<obj>", endpoint="download_file", build_only=True
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
        os.remove("output.zip")
        os.removedirs(app.config['UPLOAD_FOLDER'])
        os.removedirs("./output")
    except:
        pass
    try:
        os.mkdir(app.config['UPLOAD_FOLDER'])
        os.mkdir("./output")
    except:
        pass
    if request.method == 'POST':
        if request.form.get("objectId") == None:
            flash('No object id')
            return redirect(request.url)
        
        for i in range(len(WANTED_FILES)):
            if WANTED_FILES[i] not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files[WANTED_FILES[i]]
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = WANTED_FILES[i] + ".pdf"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', obj=request.form.get("objectId")))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <label>Abrechnung: <input type=file name=ABRG></label>
      <label>Anschreiben: <input type=file name=Anschreiben></label>
      <label>BWA: <input type=file name=BWA></label>
      <label>BEW: <input type=file name=BEW></label>
      <label>EGT: <input type=file name=EGT></label>
      <label>Objekt ID: <input type=number name=objectId></label>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/process/<obj>', methods=['GET'])
def process_data(obj):
    try:
        os.remove("ouput.zip")
    except: 
        pass
    default_runner("./upload/BWA.pdf", "./upload/ABRG.pdf", "./upload/Anschreiben.pdf", "./upload/BEW.pdf", "./upload/EGT.pdf", f"./output/{str(obj)}")
    print("Start compression")
    subprocess.run(["zip", "-r", "output.zip", "./output/"])
    return send_from_directory("./", "./output.zip", "output.zip")



if __name__ == '__main__':
    app.run()