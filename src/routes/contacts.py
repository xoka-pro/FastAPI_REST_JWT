
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db_connect import get_db
from src.database.models import User
from src.services.auth import auth_service
from src.schemas import ContactResponse, BirthdayResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(limit: int = Query(10, le=100), offset: int = 0, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)) -> List[ContactResponse]:
    """
    The read_contacts function returns a list of contacts.

    :param limit: int: Specify the maximum number of contacts that can be returned
    :param le: Limit the maximum value of the parameter
    :param offset: int: Specify the number of contacts to skip
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(query: str = Query(default='', min_length=1), db: Session = Depends(get_db),
                          current_user: User = Depends(auth_service.get_current_user)):
    """
    The search_contacts function searches for contacts in the database.

    :param query: str: Pass the search query to the function
    :param min_length: Ensure that the query string is not empty
    :param db: Session: Get the database session
    :param current_user: User: Get the user from the database
    :return: A list of contacts, which is the same as the return type for get_contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.search_contacts(query, db)
    return contacts


@router.get("/birthday/", response_model=List[BirthdayResponse])
async def get_contacts_birthday(db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_contacts_birthday function returns a list of contacts that have birthdays within the next week.
        The function takes in a database session and current user as parameters,
        which are used to query the database for
        contacts with birthdays within one week. The function then returns those contacts.

    :param db: Session: Get access to the database
    :param current_user: User: Get the current user
    :return: A list of contacts with birthdays in the next week
    :doc-author: Trelent
    """
    birthdays = await repository_contacts.get_birthdays_one_week(db)
    return birthdays


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    """
    The get_contact function is a GET request that returns the contact with the given ID.
    If no contact exists with that ID, it will return a 404 Not Found error.

    :param contact_id: int: Get the contact id from the path
    :param db: Session: Get a database session
    :param current_user: User: Get the current user from the database
    :return: A ContactResponse object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 2 requests per 10 sec',
             dependencies=[Depends(RateLimiter(times=2, seconds=10))])
async def create_contact(body: ContactResponse, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactResponse: Pass the data from the request body to the function
    :param db: Session: Access the database
    :param current_user: User: Get the current user
    :return: A ContactResponse object
    :doc-author: Trelent
    """
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactResponse, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)) -> ContactResponse:
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, and returns the updated contact.
        If no such contact exists, it raises an HTTPException with status code 404.

    :param body: ContactResponse: Pass the contact information to be updated
    :param contact_id: int: Specify the contact id of the contact to be deleted
    :param db: Session: Get the database session
    :param current_user: User: Check if the user is logged in
    :return: A ContactResponse object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_contact function removes a contact from the database.
        The function takes in an integer representing the id of the contact to be removed,
        and returns a dictionary containing information about that contact.

    :param contact_id: int: Specify the contact id of the contact to be deleted
    :param db: Session: Get a database session
    :param current_user: User: Get the current user from the database
    :return: The removed contact
    :doc-author: Trelent
    """
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
