from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# para iniciar el servidor: uvicorn main:app --reload

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

#Recuros estaticos 
app.mount("/static", StaticFiles(directory= "static"), name= "static")

@app.get("/") #aca la raiz de mi pagina web
async def root():
    return "Hola FastAPI!"

@app.get("/url") #aca colocar la barra de navegacion
async def url():
    return {"url_curso": "http://tuliobast.com/python"}

    