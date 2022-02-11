"""db module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///passwords.db', echo=True)


Base = declarative_base()


class Password(Base):  # pylint: disable=R0903
    """password table"""
    __tablename__ = 'password'
    password_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50))
    password_hash = Column(String(128))


class Configuration(Base):  # pylint: disable=R0903
    """configuration table"""
    __tablename__ = 'configuration'
    configuration_id = Column(Integer, primary_key=True, autoincrement=True)
    password_hash = Column(String(64))
    keyfile_hash = Column(String(64))
    salt = Column(String(128))


class Db:
    """db class to interact with db"""
    def __init__(self):
        mk_session = sessionmaker(bind=engine)
        mk_session = sessionmaker()
        Base.metadata.create_all(engine)
        mk_session.configure(bind=engine)
        self.session = mk_session()

    def get_passwords(self, username=None, password_id=None):
        """gets passwords from db

        if both username and password_id are none, all passwords are returned,
        otherwise will filter for one or another parameter

        Args:
            username [optional](str): if given is used to filter passwords by
                username
            password_id [optional](int): if given is used to filter passwords
                by password_id
        """
        result = None
        if not username and not password_id:
            result = self.session.query(Password).all()
        elif username:
            result = self.session.query(Password).filter(
                Password.username == username).all()
        elif password_id:
            result = self.session.query(Password).filter(
                Password.password_id == password_id).all()
        result_dict = {}
        for item in result:
            result_dict[item.id] = item.__dict__
        return result_dict

    def insert_password(self, pass_dict):
        """inserts a new password

        Args:
            pass_dict (dict): dictionary containing password to insert
        """
        password = Password(**pass_dict)
        self.session.add(password)
        self.session.commit()

    def get_configuration(self):
        """gets configuration from configuration table

        Returns:
            dict : containing configuration
        """
        result = self.session.query(Configuration).first()
        result_dict = result.__dict__
        return result_dict

    def set_configuration(self, conf_dict):
        """sets configuration (overwrites it if present)

        Args:
            conf_dict (dict): configuration to insert
        """
        nrow = self.session.query(Configuration).count()
        if nrow == 0:
            configuration = Configuration(**conf_dict)
            self.session.add(configuration)
        else:
            self.session.query(Configuration).update(conf_dict)
        self.session.commit()


def main():
    """main method for testing purposes"""
    database = Db()
    print(database.get_passwords())


if __name__ == "__main__":
    main()
