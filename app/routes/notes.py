from flask import Blueprint, request, jsonify
from ..models import Note
from ..schemas import NoteSchema
from ..extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

notes_bp = Blueprint("notes", __name__)
note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


@notes_bp.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    """
    Create a new note for the authenticated user.
    ---
    parameters:
      - in: header
        $ref: '#/securityDefinitions/Bearer'
      - in: body
        name: body
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              description: Title of the note
            content:
              type: string
              description: Content of the note
    responses:
      201:
        description: Note created successfully
        schema:
          $ref: '#/definitions/Note'
      400:
        description: Invalid input
    """
    current_user_id = get_jwt_identity()
    try:
        # Marshmallow creates a Note instance due to load_instance=True in schema
        new_note = note_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_note.user_id = current_user_id
    db.session.add(new_note)
    db.session.commit()
 
    return jsonify(note_schema.dump(new_note)), 201


@notes_bp.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    """
    Retrieve all notes for the authenticated user.
    ---
    parameters:
      - in: header
        $ref: '#/securityDefinitions/Bearer'
    responses:
      200:
        description: A list of notes
        schema:
          type: array
          items:
            $ref: '#/definitions/Note'
    """
    current_user_id = get_jwt_identity()
    user_notes = Note.query.filter_by(user_id=current_user_id).all()
    return jsonify(notes_schema.dump(user_notes)), 200


@notes_bp.route("/notes/<int:note_id>", methods=["GET"])
@jwt_required()
def get_note(note_id):
    """
    Retrieve a single note by ID for the authenticated user.
    ---
    parameters:
      - in: header
        $ref: '#/securityDefinitions/Bearer'
      - in: path
        name: note_id
        type: integer
        required: true
        description: ID of the note to retrieve
    responses:
      200:
        description: A single note object
        schema:
          $ref: '#/definitions/Note'
      404:
        description: Note not found
    """
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()

    if not note:
        return jsonify({"message": "Note not found."}), 404

    return jsonify(note_schema.dump(note)), 200


@notes_bp.route("/notes/<int:note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    # ... (the docstring remains the same) ...
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()

    if not note:
        return jsonify({"message": "Note not found."}), 404

    try:
        updated_note_data = note_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if hasattr(updated_note_data, 'title'):
        note.title = updated_note_data.title
    if hasattr(updated_note_data, 'content'):
        note.content = updated_note_data.content

    db.session.commit()

    return jsonify(note_schema.dump(note)), 200


@notes_bp.route("/notes/<int:note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    """
    Delete a note for the authenticated user.
    ---
    parameters:
      - in: header
        $ref: '#/securityDefinitions/Bearer'
      - in: path
        name: note_id
        type: integer
        required: true
        description: ID of the note to delete
    responses:
      200:
        description: Note deleted successfully
      404:
        description: Note not found
    """
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=current_user_id).first()

    if not note:
        return jsonify({"message": "Note not found."}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted."}), 200