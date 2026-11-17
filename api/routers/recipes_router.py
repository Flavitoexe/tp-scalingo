from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.Recipes import Recipes, CreateRecipe, PatchRecipe
from schemas.Users import Users
from services.recipes_services import readRecipes, readRecipe, createRecipe, updateRecipe, deleteRecipeById
from services.users_services import getCurrentUser
from database import getDb


router = APIRouter()


@router.get(
    "/recipes", 
    status_code=200
)
def getRecipes(
    db: Session = Depends(getDb)
) :
    return readRecipes(db)


@router.get(
    "/recipe/{id}", 
    status_code=200
)
def getRecipe(
    id: int,
    db: Session = Depends(getDb),
    currentUser: Users = Depends(getCurrentUser) 
) :
    return readRecipe(id, db, currentUser)


@router.post(
    "/recipe",
    status_code=201
)
def postRecipe(
    data: CreateRecipe,
    db: Session = Depends(getDb),
    currentUser: Users = Depends(getCurrentUser)
) :
    return createRecipe(data, db, currentUser)


@router.patch(
    "/recipe/{id}",
    status_code=200
)
def patchRecipe(
    id: int,
    patch: PatchRecipe,
    db: Session = Depends(getDb),
    currentUser: Users = Depends(getCurrentUser) 
) :
    return updateRecipe(id, patch, db, currentUser)


@router.delete(
    "/recipe/{id}",
    status_code=204
)
def deleteRecipe(
    id: int,
    db: Session = Depends(getDb),
    currentUser: Users = Depends(getCurrentUser)
) :
    return deleteRecipeById(id, db, currentUser)
