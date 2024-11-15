from flask import Blueprint, jsonify
from models import IncomeList
from utils import get_session

income_list_bp = Blueprint('income_list', __name__)


@income_list_bp.route('/incomelists', methods=['GET'])
def get_incomelists():
    """
    Endpoint to get all entries from the IncomeList table.

    Returns:
        A list of JSON dictionaries, each representing a row in the IncomeList table.
    """
    with get_session() as session:
        incomelists = session.query(IncomeList).all()
        return jsonify([{
            'id': incomelist.id,
            'name': incomelist.name
        } for incomelist in incomelists]), 200
