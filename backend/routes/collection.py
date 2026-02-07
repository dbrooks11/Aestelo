from extensions import db
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import (
    Collection,
    CollectionItem,
    Spot,
    SpotMedia,
    UserProfile,
    Visit,
    VisitMedia,
)
from schemas import CollectionItemSchema, CollectionSchema
from sqlalchemy import case, exists, select, update
from sqlalchemy.orm import joinedload

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

    if not (bool(spot_id) ^ bool(visit_id)):
        return jsonify({'error': 'Invalid data'}), 400
    
    if spot_id:
        Model = Spot
        item_id = spot_id
        thumbnail_query = SpotMedia.query.with_entities(SpotMedia.photo_path).filter_by(spot_id=spot_id, sort_order=1).first()
    elif visit_id:
        Model = Visit
        item_id = visit_id
        thumbnail_query = VisitMedia.query.with_entities(
                VisitMedia.photo_path
            ).filter_by(visit_id=visit_id, sort_order=1).first()

    thumbnail = thumbnail_query[0] if thumbnail_query else None

    if not thumbnail:
            raise Exception

    try:
        is_collection_owned = Collection.query.filter_by(
            id=collection_id, user_id=current_user
        ).first()

        if is_collection_owned:
            filters = {
                'collection_id': collection_id,
                'saved_by': current_user,
                'spot_id': spot_id,
                'visit_id': visit_id
            }

            filters = {k: v for k, v in filters.items() if v is not None}

            is_saved = CollectionItem.query.filter_by(**filters).first()
        else:
            return jsonify({'error': 'Collection not found'}), 404
        
        thumbnail_list = list(is_collection_owned.preview_thumbnails or []) 

        if not is_saved:
            new_collection_item = CollectionItem(
                collection_id=collection_id,
                spot_id=spot_id,
                visit_id=visit_id,
                saved_by=current_user
            )
            db.session.add(new_collection_item)

            count_update_query = (
                update(Model)
                .where(Model.id == item_id)
                .values(save_count=Model.save_count + 1)
                .returning(Model.save_count)
            )

            updated_save_count = db.session.execute(count_update_query).scalar()

            if thumbnail not in thumbnail_list:
                thumbnail_list.insert(0, thumbnail)

            is_collection_owned.preview_thumbnails = thumbnail_list[:4]

            db.session.commit()
            
            return jsonify({'message': 'Added to collection successfully',
                            'spot_save_count': updated_save_count if spot_id else None,
                            'visit_save_count': updated_save_count if visit_id else None,
                            'saved': True}), 201
        else:
            db.session.delete(is_saved)

            count_update_query = (
                update(Model)
                .where(Model.id == item_id)
                .values(save_count=case(
                    (Model.save_count > 0, Model.save_count - 1),
                    else_=0
                        )
                    )
                .returning(Model.save_count)
            )

            updated_save_count = db.session.execute(count_update_query).scalar()

            if thumbnail in thumbnail_list:
                thumbnail_list.remove(thumbnail)

            is_collection_owned.preview_thumbnails = thumbnail_list[:4]

            db.session.commit()
            return jsonify({'message': 'Removed from collection successfully',
                            'spot_save_count': updated_save_count if spot_id else None,
                            'visit_save_count': updated_save_count if visit_id else None,
                            'saved': False}), 200
    except Exception as e:
        current_app.logger.error(str(e))
        db.session.rollback()
        return jsonify({'error': 'Failed to save/unsave item'}), 500
    

@collection_bp.route('/me', methods = ['GET'])
@jwt_required()
def get_collections():
    current_user = get_jwt_identity()

    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=6, type=int)

        collections = Collection.query.filter_by(user_id=current_user)

        paginated_collections = collections.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        schema = CollectionSchema()

        result = schema.dump(paginated_collections.items, many=True)

        return jsonify({
            'collections': result,
            'total': paginated_collections.total,
            'total_pages': paginated_collections.pages,
            'current_page': paginated_collections.page
        }), 200
    except Exception as e:
        current_app.logger.error(str(e))
        db.session.rollback()
        return jsonify({'error': 'Failed to load collections'}), 500
    

@collection_bp.route('/<collection_id>/view', methods = ['GET'])
@jwt_required()
def view_collection(collection_id):
    if not collection_id:
        return jsonify({'error': 'Invalid Collection'}), 400
    
    current_user = get_jwt_identity()

    try:
        is_collection_owned = db.session.query(exists().where(Collection.id == collection_id, Collection.user_id == current_user)).scalar()

        if not is_collection_owned:
            return jsonify({'error': 'You can not access this Collection'}), 403
        
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=6, type=int)
        
        collection_items = db.paginate(
                select(CollectionItem)
                .options(joinedload(CollectionItem.spot).joinedload(Spot.user_profile).load_only(UserProfile.username),
                         joinedload(CollectionItem.visit))
                .where(CollectionItem.collection_id == collection_id)
                .order_by(CollectionItem.saved_at.desc()),
                page=page,
                per_page=per_page,
                error_out=False
        )

        schema = CollectionItemSchema()
        result = schema.dump(collection_items.items, many=True)

        return jsonify({
                'collection_items': result,
                'total': collection_items.total,
                'total_pages': collection_items.pages,
                'current_page': collection_items.page
            }), 200
    except Exception as e:
        current_app.logger.warning(str(e))
        return jsonify({'error':'Failed to fetch Collection Items'}), 500
