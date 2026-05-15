import logging

from app.config import Config
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from utils.storage import ObjectStorage
from utils.exceptions import InvalidFileTypeError, InvalidObjectStorageDestinationError

s3_bp = Blueprint('s3', __name__, url_prefix='/s3')
logger = logging.getLogger("root")


@s3_bp.route('/presigned-url/<string:content>', methods=['POST'])
@jwt_required()
def get_presigned_url(content):
    current_user = get_jwt_identity()
    storage = ObjectStorage()
    try:
        data = request.files.lists()
        presigned_urls = []

        for key, file_list in data:
            for file in file_list:
                mimetype: str | None = file.content_type
                if mimetype:
                    presigned_urls.append(storage.generate_presigned_url(mimetype=mimetype, user_id=current_user, expires_in=1800, content_target=content))
        return jsonify({'data': presigned_urls}), 200
    except InvalidFileTypeError as ifte:
        logger.error(str(ifte))
        return jsonify({'error': f"Invalid file type: {mimetype}"}), 400
    except InvalidObjectStorageDestinationError as iosde:
        logger.error(str(iosde))
        return jsonify({'error': 'Invalid destination'}), 500
    except Exception as e:
        logger.error(str(e))
        return jsonify({'error': "Failed to upload photos"}), 500

