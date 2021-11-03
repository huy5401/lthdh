from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from werkzeug.utils import secure_filename
import os
import pickle
from pre import preprocessing


app = Flask(__name__)
app.config['UPLOAD_EXTENSIONS'] = ['.txt']
app.secret_key = "btlthdh"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def submit():
    try:
        if request.method == 'POST':
            text = request.form['text_area']
            data = []
            with open('classifier_news.pkl', 'rb') as f:
                clf = pickle.load(f)
            with open('news_vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
            # if text == '' and request.files['file'].filename == '':
            #     flash('Điển vào hay là chọn file thì mới dự đoán được chứ ơ hay nhề -.-')

            if text != "":
                text = preprocessing(text)
                data.append(text)
                vec_data = vectorizer.transform(data)
                result = clf.predict(vec_data)
                return render_template('home.html', result=result[0])
            if request.files:
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
                with open(fileName, "r", encoding='utf8') as f:
                    lines = f.readlines()
                    lines = ' '.join(lines)
                lines = preprocessing(lines)
                data.append(lines)
                vec_data = vectorizer.transform(data)
                result = clf.predict(vec_data)
                return render_template('home.html', result=result[0])
    except Exception as e:
        print("\tError", e)
        flash('Điền vào hay là chọn file thì mới dự đoán được chứ ơ hay nhề -.-')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)