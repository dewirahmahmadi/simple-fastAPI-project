from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services,schemas as _schemas

import starlette.responses as _responses


app = _fastapi.FastAPI()
_services.create_database()

@app.get("/")
async def root():
    return _responses.RedirectResponse("/redoc")

@app.post("/api/v1/users/", response_model=_schemas.User)
def create_user(user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    #Check if the email exist
    if _services.is_email_exist(db=db, email=user.email):
        raise _fastapi.HTTPException(
            status_code=400, detail="The email already exists"
        )
    return _services.create_user(db=db, user=user)

@app.get("/api/v1/users/", response_model=List[_schemas.User])
def fetch_users(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users

@app.get("/api/v1/users/{user_id}", response_model=_schemas.User)
def fetch_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    #Check if the data exist
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="The user does not exists"
        )
    return db_user

@app.post("/api/v1/users/{user_id}/jobs", response_model=_schemas.Job)
def create_job(user_id: int, job: _schemas.JobCreate, db:_orm.Session = _fastapi.Depends(_services.get_db)):
    if _services.is_user_not_exists(db=db, user_id=user_id):
        raise _fastapi.HTTPException(
            status_code=404, detail="The user does not exists"
        )
    return _services.create_job(db=db, job=job, user_id=user_id)

@app.get("/api/v1/jobs", response_model=List[_schemas.Job])
def fetch_jobs(skip: int = 0, limit: int = 10, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    jobs = _services.get_jobs(db=db, skip=skip, limit=limit)
    return jobs

@app.delete("/api/v1/jobs/{job_id}")
def delete_job(job_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_job(db=db, job_id=job_id)
    return {"message": f"successfully deleted job with id: {job_id}"}

@app.put("/jobs/{job_id}", response_model=_schemas.Job)
def update_job(job_id: int, job: _schemas.JobCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.update_job(db=db, job_id=job_id, job=job)