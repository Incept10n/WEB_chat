from fastapi import Depends, HTTPException, Response
from model.entities.User import Users
from model.some import get_db
from schema import Login, Register
from sqlalchemy.orm import Session

from service.UtilityFunctions import create_access_token, hash_sha256


class AuthenticationService:
    def register(self, user: Register, db: Session = Depends(get_db)):
        db_user = db.query(Users).filter(Users.email == user.email).first()
        if (db_user):
            raise HTTPException(status_code = 401, detail="This email is already registered!")
        new_user = Users(email=user.email, passwd=hash_sha256(user.passwd))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "Users registered successfully"}

    def login(self, user: Login, response: Response, db: Session = Depends(get_db)):
        db_user = db.query(Users).filter(Users.email == user.email, Users.passwd == hash_sha256(user.passwd)).first()
        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
            )
        access_token = create_access_token(data={
            "user_id": db_user.id,
            "email": user.email
            })

        response.set_cookie(key="access_token", value=access_token, httponly=True, samesite='None')

        return {"access_token": access_token}