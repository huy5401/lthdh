from flask import Flask, render_template,request, redirect, url_for
from flask.helpers import flash
# from model.main import predict
#hjashfkasdhfaks
import pickle

app = Flask(__name__)

app.secret_key = "btlthdh"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        text = request.form['text_area']
        if text != "":
            with open('classifier_news.pkl', 'rb') as f:
                clf = pickle.load(f)

            with open('news_vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
            data = []
            # pre = preprocessing(testset['cmt'])
            data.append(text)
            newtest = vectorizer.transform(data)
            result = clf.predict(newtest)
            return render_template('home.html', text=result[0])
        else:
            flash("Điền nội dung vào mới dự đoán được chứ ơ hay -.-")
            print("please enter into text area")
            return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)