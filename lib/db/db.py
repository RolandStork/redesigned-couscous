"""db module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///passwords.db', echo=True)


Base = declarative_base()


class Password(Base):
    __tablename__ = 'password'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password_hash = Column(String(128))


class Configuration(Base):
    __tablename__ = 'configuration'
    id = Column(Integer, primary_key=True, autoincrement=True)
    password_hash = Column(String(64))
    keyfile_hash = Column(String(64))
    salt = Column(String(128))


class Db:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        Session = sessionmaker()
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
        self.session = Session()

    def get_passwords(self, username=None, id=None):
        result = None
        if not username and not id:
            result = self.session.query(Password).all()
        elif username:
            result = self.session.query(Password).filter(
                Password.username == username).all()
        elif id:
            result = self.session.query(Password).filter(
                Password.id == id).all()
        result_dict = {}
        for item in result:
            result_dict[item.id] = item.__dict__
        return result_dict

    def get_configuration(self):
        result = self.session.query(Configuration).first()
        result_dict = result.__dict__
        return result_dict


def main():
    db = Db()


if __name__ == "__main__":
    main()
