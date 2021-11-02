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
    try:
        if request.method == 'POST':
            text = request.form['text_area']
            data = []
            with open('classifier_news.pkl', 'rb') as f:
                clf = pickle.load(f)
            with open('news_vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
            if text == '' and request.files['file'].filename == '':
                flash('điển vào hay là chọn file đi ơ hay nhề')

            if text != "":
                # pre = preprocessing(testset['cmt'])
                data.append(text)
                ve_data = vectorizer.transform(data)
                result = clf.predict(ve_data)
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
                with open(fileName, "r", encoding='utf-8') as f:
                    lines = f.readlines()
                    lines = ' '.join(lines)
                print(lines)
                data.append(lines)
                ve_data = vectorizer.transform(data)
                result = clf.predict(ve_data)
                return render_template('home.html', result=result[0])

                # filename = secure_filename(fileName)
                # if filename != '':
                #     file_exten = os.path.splitext(filename)[1]
                #     print(file_exten)
                #     if file_exten not in app.config['UPLOAD_EXTENSIONS']:
                #         os.abort(400)
                # f.save(os.path.join(fileName))
                # print(f)
                # f = open(fileName,"r")
                # lines = f.readlines()
                # lines = ' '.join(lines)
                # data.append(lines)
                # print(data)
                # with open('classifier_news.pkl', 'rb') as f:
                #     clf = pickle.load(f)
                # with open('news_vectorizer.pkl', 'rb') as f:
                #     vectorizer = pickle.load(f)
                # vec_data = vectorizer.transform(data)
                # result = clf.predict(vec_data)
                # print(result)
                # return render_template('home.html', result=result[0])
    except Exception as e:
        print("\tError", e)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)