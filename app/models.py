import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import datetime as _dt

import database as _database

#SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    first_name = _sql.Column(_sql.String)
    last_name = _sql.Column(_sql.String)
    gender = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)

    jobs = _orm.relationship("Job", back_populates="owner")

class Job(_database.Base):
    __tablename__ = "jobs"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    description = _sql.Column(_sql.String, index=True)
    deadline= _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="jobs")