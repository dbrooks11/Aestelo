from flask import Blueprint, request, jsonify
from exstensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.collection import Collection, CollectionItem
from models.spot import Spot
from models.visit import Visit
from sqlalchemy import exists, case

collection_bp = Blueprint('collection', __name__, url_prefix='/collection')

@collection_bp.route('/<collection_id>', methods=['POST'])
@jwt_required()
def save_item(collection_id):

    if not collection_id:
        return jsonify({'error': 'Invalid data'}), 400
    
    current_user = get_jwt_identity()

    data = request.get_json()
    spot_id = data.get('spot_id', None)
    visit_id = data.get('visit_id', None)

    if (spot_id and visit_id) or (not spot_id and not visit_id):
        return jsonify({'error': 'Invalid data'}), 400

    try:
        is_collection_owned = db.session.query(exists().where(Collection.id == collection_id, Collection.user_id == current_user)).scalar()

        if is_collection_owned:
            if spot_id:
                is_saved = CollectionItem.query.filter_by(spot_id=spot_id, saved_by=current_user, collection_id=collection_id).first()
            elif visit_id:
                is_saved = CollectionItem.query.filter_by(visit_id=visit_id, saved_by=current_user, collection_id=collection_id).first()
        else:
            return jsonify({'error': 'Collection does not exist'}), 404

        if not is_saved:
            new_collection_item = CollectionItem(
                collection_id=collection_id,
                spot_id=spot_id,
                visit_id=visit_id,
                saved_by=current_user
            )
        
            db.session.add(new_collection_item)

            if spot_id:
                Spot.query.filter_by(id=spot_id).update({
                    'save_count': case(
                        (Spot.save_count == 0, 1),
                        else_=(Spot.save_count + 1)
                    )
                })
            elif visit_id:
                Visit.query.filter_by(id=visit_id).update({
                    'save_count': case(
                        (Visit.save_count == 0, 1),
                        else_=(Visit.save_count + 1)
                    )
                })
            
            db.session.commit()

            if spot_id:
                data = Spot.query.with_entities(Spot.save_count).filter_by(id=spot_id).first()
            elif visit_id:
                data = Visit.query.with_entities(Visit.save_count).filter_by(id=visit_id).first()

            return jsonify({'message': 'Added to collection successfully',
                            'spot_save_count': data[0] if spot_id else None,
                            'visit_save_count': data[0] if visit_id else None,
                            'saved': True}), 201
        else:
            db.session.delete(is_saved)

            if spot_id:
                Spot.query.filter_by(id=spot_id).update({
                    'save_count': case(
                        (Spot.save_count == 0, 0),
                        else_=(Spot.save_count - 1)
                    )
                })
            elif visit_id:
                Visit.query.filter_by(id=visit_id).update({
                    'save_count': case(
                        (Visit.save_count == 0, 0),
                        else_=(Visit.save_count - 1)
                    )
                })
            db.session.commit()

            if spot_id:
                data = Spot.query.with_entities(Spot.save_count).filter_by(id=spot_id).first()
            elif visit_id:
                data = Visit.query.with_entities(Visit.save_count).filter_by(id=visit_id).first()
            return jsonify({'message': 'Removed from collection successfully',
                            'spot_save_count': data[0] if spot_id else None,
                            'visit_save_count': data[0] if visit_id else None,
                            'saved': False}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500