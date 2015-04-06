from bottle import route, run, request

import os
import uuid

STORAGE = "traces"


@route('/log', method='POST')
def log():
    name = request.forms.name
    data = request.files.data
    if name and data:
        storepath = os.path.join(STORAGE,name)
        if not os.path.exists(STORAGE):
            os.mkdir(STORAGE)
        if not os.path.exists(storepath):
            os.mkdir(storepath)
        tracepath = os.path.join(storepath, str(uuid.uuid4())+".trace")
        with open(tracepath,'w+') as fp:
            data.save(fp)
    return "Look how clever you are!"
    
    
if __name__ == "__main__":
    run(host='0.0.0.0', port=11234)