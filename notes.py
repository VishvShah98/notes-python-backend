from flask import Blueprint, request, jsonify
from models import Note, db
from decorators import token_required

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/notes', methods=['GET'])
@token_required
def get_all_notes(current_user):
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'content': note.content, 'id': note.id} for note in notes]), 200


@notes_bp.route('/notes', methods=['POST'])
@token_required
def create_note(current_user):
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required.'}), 400

    new_note = Note(content=content, user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({'message': 'Note created successfully.'}), 201


@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
@token_required
def update_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Content is required.'}), 400

    note.content = content
    db.session.commit()

    return jsonify({'message': 'Note updated successfully.'}), 200


@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@token_required
def delete_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({'message': 'Note deleted successfully.'}), 200