from pyvi import ViTokenizer
# from nltk.corpus import stopwords
import re

stopwords = set()
with open('vietnamese.txt', 'r', encoding='utf8') as f:
    line = f.readline()
    while line:
        line = f.readline().strip('\n')
        stopwords.add(line)


def clear_text(text):
    text = re.sub(r"[^aàáảãạâầấẩẫậăằắẳẵặeèéẻẽẹêềếểễệbcđdiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuưùúủũụưừứửữựyỳýỷỹỵgphklmnvstrxqAÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶEÈÉẺẼẸÊỀẾỂỄỆÊĐDIÌÍỈĨỊOÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢUÙÚỦŨỤƯỪỨỬỮỰYỲÝỶỸỴÂĂĐÔƠƯGHKLTMNVSPXYQBC0-9]", " ", text)
    return text


def lowercase(text):
    return text.lower()


def tokenize(text):
    return ViTokenizer.tokenize(text)


def remove_stopwords(text):
    doc_words = []
    text = tokenize(text)
    text = text.split()
    for word in text:
        if word not in stopwords:
            doc_words.append(word)
    doc_text = ' '.join(doc_words).strip()
    return doc_text


def preprocessing(text):
    temp = clear_text(text)
    temp = lowercase(temp)
    temp = remove_stopwords(temp)
    return temp
