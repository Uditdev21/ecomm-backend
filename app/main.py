from fastapi import FastAPI
from .test import testRouts
from .admin import admin
from .db import db
from .client import client
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(client,prefix='/client')
app.include_router(admin,prefix='/admin')
app.include_router(testRouts,prefix='/test')

@app.get('/')
def root():
    return "server running"