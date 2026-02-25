import datetime
from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class VoterRegDeadline(Base):
    __tablename__ = "voter_reg_deadline"

    state: Mapped[str] = mapped_column(String(30), primary_key=True)
    deadline_by_mail: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    deadline_in_person: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    deadline_online: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    election_day_registration: Mapped[str] = mapped_column(String, nullable=True)
    online_registration_link: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(String)

    @validates('deadline_in_person')
    @validates('deadline_by_mail')
    @validates('deadline_online')
    def empty_string_to_null(self, key, value):
        if isinstance(value,str) and value == '':
            return None
        else:
            return value

    def serialize(self):
        return {
            'state': self.state,
            'deadline_by_mail': self.deadline_by_mail,
            'deadline_in_person': self.deadline_in_person,
            'deadline_online': self.deadline_online,
            'election_day_registration': self.election_day_registration,
            'online_registration_link': self.online_registration_link,
            'description': self.description
        }

    def __repr__(self) -> str:
        return f"VoterRegDeadline(state={self.state})"