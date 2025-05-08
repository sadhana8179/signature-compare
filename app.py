from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from models.compare import compare_signatures
from database.database import init_db, save_result, get_all_results

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        original = request.files['original']
        test = request.files['test']
        orig_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(original.filename))
        test_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(test.filename))
        original.save(orig_path)
        test.save(test_path)

        similarity = compare_signatures(orig_path, test_path)
        save_result(original.filename, test.filename, similarity)
        result = f"Similarity Score: {similarity}%"
    return render_template('index.html', result=result)

@app.route('/dashboard')
def dashboard():
    results = get_all_results()
    return render_template('dashboard.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)




