import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import ContactResponse, BirthdayResponse
from src.repository.contacts import (
    create_contact,
    get_contacts,
    get_contact_by_id,
    update_contact,
    remove_contact,
    search_contacts,
    get_birthdays_one_week)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.fake_user = Contact(
            id=1, first_name='John', last_name='Doe', birthday='1988-02-01',
            email='john@doe.com', phone='0661234567', other_info='test',
            created_at='2021-02-01', updated_at='2021-02-01')

    def tearDown(self):
        del self.session
        del self.user
        del self.fake_user

    async def test_create_contact(self):
        body = ContactResponse(id=1, first_name='John', last_name='Doe', birthday='1988-02-01',
                               email='john@doe.com', phone='0661234567', other_info='test',
                               created_at='2021-02-01', updated_at='2021-02-01')
        result = await create_contact(body=body, db=self.session)
        self.assertEqual(result.id, body.id)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.other_info, body.other_info)
        self.assertTrue(hasattr(result, 'id'))

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_id(contact_id=contact.id, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await get_contact_by_id(contact_id=0, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact(self):
        body = Contact(id=1, first_name='John', last_name='Doe', birthday='1988-02-01',
                       email='john@doe.com', phone='0661234567', other_info='test')
        self.session.query().filter_by().first.return_value = body
        result = await update_contact(body=body, contact_id=1, db=self.session)
        self.assertEqual(result, body)

    async def test_update_contact_not_found(self):
        body = Contact(id=1, first_name='John', last_name='Doe', birthday='1988-02-01',
                       email='john@doe.com', phone='0661234567', other_info='test')
        self.session.query().filter_by().first.return_value = None
        result = await update_contact(body=body, contact_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_remove_contact(self):
        body = Contact()
        self.session.query().filter_by().first.return_value = body
        result = await remove_contact(contact_id=1, db=self.session)
        self.assertEqual(result, body)

    async def test_remove_contact_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await remove_contact(contact_id=1, db=self.session)
        self.assertIsNone(result)

    async def test_search_contacts(self):
        body = [Contact(), Contact()]
        self.session.query().filter().all.return_value = body
        result = await search_contacts(query="1", db=self.session)
        self.assertEqual(result, body)

    async def test_get_birthdays_one_week(self):
        contacts = [Contact(id=1, first_name='John', last_name='Doe', birthday='1988-05-01')]
        contacts_birthday = [BirthdayResponse(id=1, first_name='John', last_name='Doe', birthday='1988-05-01')]
        self.session.query().filter().all.return_value = contacts
        result = await get_birthdays_one_week(db=self.session)
        self.assertEqual(contacts_birthday, result)


if __name__ == "__main__":
    unittest.main()
