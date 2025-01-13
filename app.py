from flask import Flask, jsonify, request
from tasks import add

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add_numbers():
    # Extract numbers from request
    data = request.get_json()
    x = data.get('x', 0)
    y = data.get('y', 0)

    # Call the Celery task asynchronously
    task = add.delay(x, y)

    # Return task ID to check status/result later
    return jsonify({'task_id': task.id}), 202

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    # Fetch result of the Celery task
    task = add.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return jsonify({'status': task.state, 'result': task.result}), 200
    elif task.state == 'PENDING':
        return jsonify({'status': task.state}), 202
    else:
        return jsonify({'status': task.state, 'error': str(task.info)}), 400

if __name__ == '__main__':
    app.run(debug=True)
