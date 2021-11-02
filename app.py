from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from werkzeug.utils import secure_filename
import os
# from model.main import predict
#hjashfkasdhfaks
import pickle


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.txt', '.doc', '.docx']
app.secret_key = "btlthdh"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        text = request.form['text_area']
        with open('classifier_news.pkl', 'rb') as f:
                clf = pickle.load(f)
        with open('news_vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
        data = []
        result = ''
        if text != "":  
            # pre = preprocessing(testset['cmt'])
            data.append(text)
            ve_data = vectorizer.transform(data)
            result = clf.predict(ve_data)
        elif request.files:
            f = request.files['file']
            fileName = f.filename
            filename = secure_filename(fileName)
            if filename != '':
                file_exten = os.path.splitext(filename)[1]
                print(file_exten)
                if file_exten not in app.config['UPLOAD_EXTENSIONS']:
                    os.abort(400)
            f.save(os.path.join(fileName))
            print(f)
            f = open(fileName,"r")
            lines = f.readlines()
            lines = ' '.join(lines)
            data.append(lines)
            vec_data = vectorizer.transform(data)
            result = clf.predict(vec_data)
            return redirect(request.url)

        else:
            flash("Điền nội dung vào mới dự đoán được chứ ơ hay -.-")
            print("please enter into text area")
            return redirect(url_for('home'))
    return render_template('home.html', result=result[0])

if __name__ == '__main__':
    app.run(debug=True)