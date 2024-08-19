from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='dgeison', email='dgeison@gmail.com', password='senha'
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'dgeison@gmail.com')
    )

    assert result.username == 'dgeison'
