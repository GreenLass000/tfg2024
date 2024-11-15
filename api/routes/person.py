from datetime import timezone, datetime
from flask import Blueprint, jsonify, request
from models import Person
from utils import get_session

person_bp = Blueprint('person', __name__)


@person_bp.route('/persons', methods=['GET'])
def get_persons():
    """
    Endpoint to get all persons.

    Returns:
        A list of JSON dictionaries, each representing a row in the Person table.
    """
    with get_session() as session:
        persons = session.query(Person).all()
        return jsonify([{
            'id': person.id,
            'firstName': person.firstName,
            'lastName': person.lastName,
            'isconcertado': person.isconcertado,
            'isactive': person.isactive,
            'date_joined': person.date_joined,
            'date_left': person.date_left
        } for person in persons]), 200


@person_bp.route('/persons/active', methods=['GET'])
def get_active_persons():
    """
    Endpoint to get all active persons (isactive = true).

    Returns:
        A list of JSON dictionaries, each representing a row in the Person table.
    """
    with get_session() as session:
        active_persons = session.query(Person).filter_by(isactive=True).all()
        return jsonify([{
            'id': person.id,
            'firstName': person.firstName,
            'lastName': person.lastName,
            'isconcertado': person.isconcertado,
            'isactive': person.isactive,
            'date_joined': person.date_joined,
            'date_left': person.date_left
        } for person in active_persons]), 200


@person_bp.route('/persons', methods=['POST'])
def add_person():
    """
    Endpoint to add a new person.

    Expected JSON data:
        - firstName: str
        - lastName: str
        - isConcertado: bool

    Returns:
        A JSON dictionary with the details of the added person.
    """
    data = request.get_json()
    if 'firstName' not in data or 'lastName' not in data or 'isConcertado' not in data:
        return jsonify({
            'error': 'Missing required fields'
        }), 400

    new_person = Person(
        firstName=data['firstName'],
        lastName=data['lastName'],
        isconcertado=data['isConcertado'],
        isactive=True,
        date_joined=datetime.now(timezone.utc),
    )
    with get_session() as session:
        session.add(new_person)
        session.commit()
        # Refresh the instance to ensure attributes are available
        session.refresh(new_person)

    return jsonify({
        'id': new_person.id,
        'firstName': new_person.firstName,
        'lastName': new_person.lastName,
        'isconcertado': new_person.isconcertado,
        'isactive': new_person.isactive,
        'date_joined': new_person.date_joined,
        'date_left': new_person.date_left
    }), 201


@person_bp.route('/person/delete/<int:id>', methods=['PATCH'])
def delete_person(id):
    """
    Endpoint to 'delete' a person by setting isactive to false and setting date_left.

    URL parameters:
        - id: int

    Returns:
        A JSON dictionary with the details of the updated person or an error if the person is not found.
    """
    with get_session() as session:
        person = session.query(Person).get(id)
        if person is None:
            return jsonify({
                'error': 'Person not found'
            }), 404

        if not person.isactive:
            return jsonify({
                'error': 'Person is already inactive'
            }), 400

        person.isactive = False
        person.date_left = datetime.now(timezone.utc)

        session.commit()

        return jsonify({
            'id': person.id,
            'firstName': person.firstName,
            'lastName': person.lastName,
            'isconcertado': person.isconcertado,
            'isactive': person.isactive,
            'date_joined': person.date_joined,
            'date_left': person.date_left
        }), 204
