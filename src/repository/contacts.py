from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.sql import extract

from src.database.models import Contact
from src.schemas import ContactResponse, BirthdayResponse


async def create_contact(body: ContactResponse, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact)
    contacts = contacts.limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def update_contact(body: ContactResponse, contact_id: int, db: Session):
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
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, db: Session):
    contacts = db.query(Contact).filter(
        (Contact.first_name.contains(query)) |
        (Contact.last_name.contains(query)) |
        (Contact.email.contains(query))
    ).all()
    return contacts


async def get_birthdays_one_week(db: Session):
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
