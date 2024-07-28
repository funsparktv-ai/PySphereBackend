from flask import Flask, request, jsonify
import subprocess
import sys
import io
import contextlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes


@app.route('/execute_code', methods=['POST'])
def execute_code() :
    data = request.json
    code = data.get('code')

    if not code :
        return jsonify({'success' : False, 'error' : 'No code provided'}), 400

    # Redirect stdout and stderr to capture output
    output = io.StringIO()
    error = io.StringIO()
    try :
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error) :
            exec(code, globals())
        return jsonify({'success' : True, 'output' : output.getvalue(), 'error' : error.getvalue()}), 200
    except Exception as e :
        return jsonify({'success' : False, 'error' : str(e)}), 500


@app.route('/install_package', methods=['POST'])
def install_package():
    data = request.json
    package_name = data.get('package')

    if not package_name:
        return jsonify({'success': False, 'error': 'No package name provided'}), 400

    try:
        # Installing the package using pip
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
        return jsonify({'success': True}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__' :
    app.run(debug=False)
