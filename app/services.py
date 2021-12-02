import sqlalchemy.orm as _orm

import models as _models, schemas as _schemas, database as _database

def create_database():
    """Create SQLite database"""
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    """Create database session"""
    db = _database.SessionLocal()
    try: 
        yield db
    finally:
        db.close()

def is_email_exist(db: _orm.Session, email: str):
    """Check if the email exist"""
    email = get_user_by_email(db=db, email=email)
    if email:
        return True

def is_user_not_exists(db: _orm.Session, user_id: int):
    """Check user if its not exists"""
    user = get_user(db=db, user_id=user_id)
    if user is None:
        return True

def get_user(db: _orm.Session, user_id: int):
    """Get User"""
    return db.query(_models.User).filter(_models.User.id == user_id).first()

def get_user_by_email(db: _orm.Session, email: str): 
    """Check user by email"""
    return db.query(_models.User).filter(_models.User.email == email).first()

def create_user(db: _orm.Session, user: _schemas.UserCreate):
    """Create database"""
    db_user = _models.User(email=user.email, first_name=user.first_name, last_name=user.last_name, gender=user.gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: _orm.Session, skip: int = 0, limit: int = 100):
    """Get All users"""
    return db.query(_models.User).offset(skip).limit(limit).all()

def create_job(db: _orm.Session, job: _schemas.JobCreate, user_id: int):
    """Create Job"""
    job = _models.Job(**job.dict(), owner_id=user_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def get_jobs(db: _orm.Session, skip: int = 0, limit: int = 10):
    """Get All Jobs"""
    return db.query(_models.Job).offset(skip).limit(limit).all()

def get_job(db: _orm.Session, job_id: int):
    """Get Job"""
    return db.query(_models.Job).filter(_models.Job.id == job_id).first()

def delete_job(db: _orm.Session, job_id: int):
    """Delete Job"""
    db.query(_models.Job).filter(_models.Job.id == job_id).delete()
    db.commit()

def update_job(db: _orm.Session, job_id: int, job: _schemas.JobCreate):
    """Delete Job"""
    db_job = get_job(db=db, job_id=job_id)
    db_job.title = job.title
    db_job.description = job.description
    db_job.deadline = job.deadline
    db.commit()
    db.refresh(db_job)
    return db_job