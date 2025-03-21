from fastapi import FastAPI
from databases import postgreSql
from controllers import userAuthController, bookController, borrowController

postgreSql.create_tables()

app = FastAPI()
app.include_router(userAuthController.router, prefix="/api")
app.include_router(bookController.router, prefix="/api")
app.include_router(borrowController.router, prefix="/api")