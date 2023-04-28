import unittest
from unittest.mock import MagicMock


from sqlalchemy.orm import Session

from src.database.models import User, Contact
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.test_user = User(
            id=1,
            username='SuperUser',
            email='user@super.com',
            password='superpwd',
            confirmed=True,
            avatar='https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50',
        )

    async def test_get_user_by_email(self):
        user = self.test_user
        self.session.query().filter_by().first.return_value = user
        result = await get_user_by_email(email=self.test_user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        body = UserModel(
            username=self.test_user.username,
            email=self.test_user.email,
            password=self.test_user.password,
        )
        result = await create_user(body=body, db=self.session)

        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_confirmed_email(self):
        result = await confirmed_email(email=self.test_user.email, db=self.session)
        self.assertIsNone(result)

    async def test_update_token(self):
        user = self.test_user
        token = None
        result = await update_token(user=user, refresh_token=token, db=self.session)
        self.assertIsNone(result)

    async def test_update_avatar(self):
        url = 'https://res.cloudinary.com/de4xjjvsu/image/upload/c_fill,h_250,w_250/v1682264781/web9/a12df1dcbb38'
        user = self.test_user
        result = await update_avatar(email=self.test_user.email, url=url, db=self.session)
        self.assertEqual(result.avatar, url)


if __name__ == '__main__':
    unittest.main()