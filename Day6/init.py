from app import app
from models import db, User
from werkzeug.security import generate_password_hash as gph

# name, email, password
users = [
    ("Ankit", 'user1', 'u1'),
    ("Ram", 'user2', 'u2'),
    ("Shyam", 'user3', 'u3'),
]

creators = [
    ("Alice", 'creator1', 'c1'),
    ("Tom", 'creator2', 'c2'),
    ("Jerry", 'creator3', 'c3'),
]


# Object of User == one row of User
u = User(name="Dragon", email='admin', password=gph('a'), isAdmin=True)
db.session.add(u)
db.session.commit()

for n, e, p in users:
    u = User(name=n, email=e, password=gph(p))
    db.session.add(u)
    db.session.commit()

for n, e, p in creators:
    u = User(name=n, email=e, password=gph(p), isCreator=True)
    db.session.add(u)
    db.session.commit()