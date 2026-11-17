from fastapi import FastAPI

from database import Base, engine
from routers.recipes_router import router as recipesRouter
from routers.users_router import router as usersRouter


app = FastAPI(
    title="Recipes API"
)

Base.metadata.create_all(bind=engine)

app.include_router(recipesRouter)
app.include_router(usersRouter)


@app.get("/root")
def test() :
    return {
        "message" : "API is running."
    }