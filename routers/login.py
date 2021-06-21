from fastapi import APIRouter,Depends,status
from .. import schemas,database,models
from sqlalchemy.orm import Session
from ..hashing import Hash


router=APIRouter(
      tags=['login'])

@router.post('/login')
def login(request:schemas.Login,db:Session=Depends(database.get_db)):
      user=db.query(models.Admin).filter(models.Admin.email_id==request.email_id).first()
      if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
      return user
