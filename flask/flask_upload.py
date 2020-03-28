
from flask import request,Flask

app=Flask(__name__)


@app.route('/upload',methods=["POST"])
def upload():
    upload_file = request.files.get('file')
    if upload_file is None:
        return "no file upload"

    with open('../myupload', 'wb') as f:
        data = upload_file.read()
        f.write(data)
    return "ile upload success"
app.run()
