from fastapi import  APIRouter
from .. import schemas,database,models
from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from ..database import engine, SessionLocal,get_db
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, EmailStr
from fastapi import BackgroundTasks, UploadFile, File, Form
from starlette.responses import FileResponse, JSONResponse
from starlette.requests import Request


router=APIRouter(
      tags=['Email_Sending']
      )



html = """
<html>
<head>
    <meta charset="UTF-8">
    <title>Hall Ticket</title>
</head>
<body>

<h1 style="border:rgb(0, 132, 255); border-width:5px; border-style:solid; border-bottom: hidden; text-align:center; background-color: skyblue; color:white;  padding: 0px; margin: 0px">MSIT Admissions</h1>
<p style="border: rgb(0, 132, 255); border-width:5px; border-style: ridge; text-align:lift; background-color: white; color: black; padding: 50px; margin: 0px;">Student Name: <br> <br> Exam date & time are given below <br> please go through the attachments</p>

</body>

</html>
"""

@router.get('/GatHallticket_email', status_code=status.HTTP_201_CREATED)
async def simple_send(
      file: UploadFile = File(...),
      file2: UploadFile = File(...),
      db: Session=Depends(get_db)
      ) -> JSONResponse:
      
      users=db.query(models.GatHallticket).all()
      
      for i in range(len(users)):
            message = MessageSchema(
                  subject="MSIT Hallticket 2021",
                  recipients=[users[i].email_id],
                  body=html,
                  attachments=[file,file2],
                  subtype="html"
                  )

            fm = FastMail(conf)
            await fm.send_message(message)

      return JSONResponse(status_code=200, content={"message": "email has been sent"}) 
