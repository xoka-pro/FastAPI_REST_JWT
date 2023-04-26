from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Contact
from src.schemas import ContactResponse, BirthdayResponse


async def create_contact(body: ContactResponse, db: Session):
    """
    The create_contact function creates a new contact in the database.
    Args:
        body (ContactResponse): The contact to be created.

    :param body: ContactResponse: Create a new contact object
    :param db: Session: Pass the database session to the function
    :return: The contact that was created
    :doc-author: Trelent
    """

    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(limit: int, offset: int, db: Session):
    """
    The get_contacts function returns a list of contacts from the database.
        Args:
            limit (int): The number of contacts to return.
            offset (int): The number of contacts to skip before returning results.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Skip the first n number of contacts
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact)
    contacts = contacts.limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on its id.
    Args:
        contact_id (int): The id of the desired contact.
        db (Session): A connection to the database.

    :param contact_id: int: Specify the id of the contact to be returned
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def update_contact(body: ContactResponse, contact_id: int, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactResponse): The updated contact information.
            contact_id (int): The id of the contact to update.

    :param body: ContactResponse: Get the data from the request body
    :param contact_id: int: Identify the contact to be updated
    :param db: Session: Connect to the database
    :return: The contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.other_info = body.other_info
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.

    :param contact_id: int: Specify the id of the contact to be removed
    :param db: Session: Pass in the database session object
    :return: The contact that was deleted
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session):
    """
    The search_contacts function searches the database for contacts that match a given query.

    :param query: str: Search the database for a contact
    :param db: Session: Pass the database session to the function
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = db.query(Contact).filter(
        (Contact.first_name.contains(query)) |
        (Contact.last_name.contains(query)) |
        (Contact.email.contains(query))
    ).all()
    return contacts


async def get_birthdays_one_week(db: Session):
    """
    The get_birthdays_one_week function returns a list of contacts whose birthdays are within the next week.

    :param db: Session: Pass the database session to the function
    :return: A list of BirthdayResponse objects
    :doc-author: Trelent
    """
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day)
        & (extract('month', Contact.birthday) == end_date.month) & (extract('day', Contact.birthday) <= end_date.day)
    ).all()
    return [
        BirthdayResponse(
            id=contact.id,
            first_name=contact.first_name,
            last_name=contact.last_name,
            birthday=contact.birthday
        )
        for contact in contacts
    ]
