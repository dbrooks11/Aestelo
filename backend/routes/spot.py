from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from util.photo_processing import photo_processing, get_decimal_coordinates
from util.validation import photo_validation
from util.storage import upload_to_r2, generate_presigned_url


spot_bp = Blueprint('spot', __name__, url_prefix='/spot')

@spot_bp.route('/presigned-url', methods=['POST'])
@jwt_required()
def get_presigned_url_spot():
    current_user = get_jwt_identity()
    data = request.get_json()
    presigned_urls = []

    try:
        for metadata in data:
            filename = metadata.get('fileName')
            filetype = metadata.get('fileType')
            if(filename):
                presigned_urls.append(generate_presigned_url(filename=filename, filetype=filetype, user_id=current_user, folder='quarantine_spot'))
        return jsonify({'message': presigned_urls}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@spot_bp.route('/create', methods = ['POST'])
@jwt_required()
def create_spot():
    current_user = get_jwt_identity()

    try:
        data = request.get_json()

        print(data)

        return jsonify({'message': 'done'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500