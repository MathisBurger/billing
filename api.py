from flask import Flask, flash, redirect, request, send_from_directory, url_for
from main import default_runner
import os
import subprocess

# static values
UPLOAD_FOLDER = "./upload"
ALLOWED_EXTENSIONS = {'pdf'}
WANTED_FILES = ["ABRG", "Anschreiben", "BWA", "BEW", "EGT", "JOURNAL", "RL", "VB", "WP_EINZEL"]

# Creates basic flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.add_url_rule(
    "/process/<obj>", endpoint="download_file", build_only=True
)

# Checks if a file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Default file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():

    # Removes unnessesary data
    try:
        os.remove("output.zip")
        os.removedirs(app.config['UPLOAD_FOLDER'])
        os.removedirs("./output")
    except:
        pass

    # Creates all wanted directories
    try:
        os.mkdir(app.config['UPLOAD_FOLDER'])
        os.mkdir("./output")
    except:
        pass

    if request.method == 'POST':
        if request.form.get("objectId") == None:
            flash('No object id')
            return redirect(request.url)
        
        # Saves all files 
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
      <label>Journal: <input type=file name=JOURNAL></label>
      <label>RL: <input type=file name=RL></label>
      <label>VB: <input type=file name=VB></label>
      <label>WP Einzel: <input type=file name=WP_EINZEL></label>
      <label>Objekt ID: <input type=number name=objectId></label>
      <input type=submit value=Upload>
    </form>
    '''

# processes all the data
@app.route('/process/<obj>', methods=['GET'])
def process_data(obj):
    try:
        os.remove("ouput.zip")
    except: 
        pass
    try:
        default_runner("./upload/BWA.pdf", "./upload/ABRG.pdf", "./upload/Anschreiben.pdf", "./upload/BEW.pdf", "./upload/EGT.pdf", "./upload/JOURNAL.pdf", "./upload/RL.pdf", "./upload/VB.pdf", "./upload/WP_EINZEL.pdf", "./upload/SONSTIGE.pdf", f"./output/{str(obj)}")
    except:
        return "Cannot process data"
    print("Start compression")
    subprocess.run(["zip", "-r", "output.zip", "./output/"])
    return send_from_directory("./", "./output.zip", "output.zip")



if __name__ == '__main__':
    app.run()