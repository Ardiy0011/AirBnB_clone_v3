from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON response with status OK."""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats')
def obj_number():
    """Retrieve the number of objects by type."""
