import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_headers(headers):
    apikey = headers.get('apikey', None)
    host = headers.get('Host', None)
    return apikey, host

@app.route('/v1/uploadfile', methods=['POST'])
def upload_file():
    apikey, host = get_headers(request.headers)
    if not apikey or not host:
        return jsonify({'error': 'Headers no especificados'}), 401

    uploaded_file = request.files['file']
    if not uploaded_file:
        return jsonify({'error': 'Archivo no encontrado en el formulario'}), 400

    data = {
        'bucket': request.form.get('bucket', ''),
        'folder': request.form.get('folder', '') #TODO: aqui va el otorgante_id/uuid/transaction_id
    }
    headers = {
        'apikey': apikey,
        'Host': host
    }
    api_url = 'https://api.devdicio.net:8444/v1/sec_dev_file'

    try:
        response = requests.post(
            api_url,
            headers=headers,
            data=data,
            files={'file': uploaded_file}
        )
        if response.status_code == 200:
            resultado = response.json()
            return jsonify(resultado), 200
        else:
            return jsonify({'error': 'Error en la API externa'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/v1/file', methods=['GET'])
def list_file():
    apikey, host = get_headers(request.headers)
    if not apikey or not host:
        return jsonify({'error': 'Headers no especificados'}), 401

    headers = {
        'apikey': apikey,
        'Host': host
    }
    params = {
        'bucket': request.args.get('bucket', ''),
        'folder': request.args.get('folder', ''),
        'order':  request.args.get('order', ''),
        'pv': request.args.get('pv', '')
    }
    api_url = 'https://api.devdicio.net:8444/v1/sec_dev_filter_bucket'

    try:
        response = requests.get(
            api_url,
            headers=headers,
            params=params
        )
        if response.status_code == 200:
            resultado = response.json()
            return jsonify(resultado), 200
        else:
            return jsonify({'error': 'Error en la API externa'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8444)