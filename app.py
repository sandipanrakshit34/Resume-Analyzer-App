from flask import Flask, render_template, request
import PyPDF2
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab')
nltk.download('stopwords')

app = Flask(__name__)

# Keywords for matching
keywords = ["python", "data analysis", "machine learning", "deep learning",
            "artifical intelligence", "nlp", "keras", "tensorflow", "r", "sql"]

stop_words = set(stopwords.words('english'))

def extract_PDF(file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(file)
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

def extract_tokens(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    return [token for token in tokens if token not in stop_words]

def match_keywords(tokens):
    return [word for word in tokens if word in keywords]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['resume']
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            text = extract_PDF(uploaded_file)
            tokens = extract_tokens(text)
            matched = match_keywords(tokens)
            score = len(matched)
            return render_template('result.html', matched=matched, score=score, total=len(keywords))
        else:
            return "Only PDF files are supported."
    return render_template('index.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

