from pydantic import EmailStr

from esmerald.contrib.auth.tortoise.base_user import User as BaseUser


class User(BaseUser):
    """
    Inherits from the BaseUser all the fields and adds extra unique ones.
    """

    def __str__(self):
        return f"{self.email} - {self.last_login}"


async def create_superuser(
    first_name: str, last_name: str, username: str, email: EmailStr, password: str
) -> User:
    """
    Creates a superuser in the database.
    """
    user = await User.create_superuser(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user
