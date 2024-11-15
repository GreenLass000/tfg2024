from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base, Person, IncomeList, SpentList

# Crear el motor y la sesión de SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def get_session():
    """
    Creates and returns a new SQLAlchemy session.

    Returns:
        Session: A new instance of SQLAlchemy session.
    """
    return Session()


def init_db():
    """
    Initializes the database by creating all tables defined in the models,
    verifies or creates the person 'Caja Economia', and verifies or creates the elements in IncomeList and SpentList.
    """
    # Create all tables
    with engine.connect() as connection:
        Base.metadata.create_all(bind=engine)

    # Creates a new session and adds the necessary elements to the database
    with get_session() as session:
        try:
            # Check if the person 'Caja Economia' exists
            person = session.query(Person).filter_by(
                firstName="Caja", lastName="Economia").first()
            if not person:
                # Create the person if it does not exist
                new_person = Person(
                    firstName="Caja",
                    lastName="Economia",
                    isconcertado=False,
                    isactive=True,
                    date_joined=datetime.utcnow()
                )
                session.add(new_person)
                session.commit()
                print("Person 'Caja Economia' created.")
            else:
                print("Person 'Caja Economia' already exists.")

            # Check if the IncomeList table is empty
            income_list_count = session.query(IncomeList).count()
            if income_list_count == 0:
                # Add items to IncomeList
                income_items = [
                    "Aportacion Familiar",
                    "Propios",
                    "Traspaso Administracion",
                    "Otros"
                ]
                for item in income_items:
                    formatted_item = item.capitalize()
                    new_income_item = IncomeList(name=formatted_item)
                    session.add(new_income_item)
                session.commit()
                print("Items added to IncomeList.")
            else:
                print("IncomeList already contains items.")

            # Check if the SpentList table is empty
            spent_list_count = session.query(SpentList).count()
            if spent_list_count == 0:
                # Add items to SpentList
                spent_items = [
                    ("PELUQUERIA", False),
                    ("ALIMENTACIÓN", True),
                    ("FARMACIA", True),
                    ("HIGIENE", True),
                    ("OCIO Y TIEMPO LIBRE", True),
                    ("ROPA", True),
                    ("TRANSPORTE", True),
                    ("PAPELERIA", True),
                    ("OTROS", True)
                ]
                for name, isconcertado in spent_items:
                    formatted_name = name.capitalize()
                    new_spent_item = SpentList(
                        name=formatted_name, isconcertado=isconcertado)
                    session.add(new_spent_item)
                session.commit()
                print("Items added to SpentList.")
            else:
                print("SpentList already contains items.")
        except Exception as e:
            session.rollback()
            print(f"Error checking or creating items: {e}")
