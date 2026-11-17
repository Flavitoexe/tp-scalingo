from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from database import getDb
from schemas.Recipes import CreateRecipe, PatchRecipe
from schemas.Users import Users
from models.Recipes import Recipes


def readRecipes(
    db: Session 
) :
    
    recipes = db.query(Recipes)

    return {
        "recipes": recipes.all()
    }


def readRecipe(
        id: int,
        db: Session,
        currentUser: Users
) :
    
    recipe = db.query(Recipes).filter(Recipes.id == id).first()
    if recipe is None :
        raise HTTPException(
            status_code=404,
            detail="No recipe with this id."
        )

    isOwner = recipe.ownerId == currentUser.id
    if not isOwner :
        raise HTTPException(
            status_code=403,
            detail="Can't read another one's recipe."
        )

    return {
        "recipe": recipe 
    }


def createRecipe(
    data: CreateRecipe,
    db: Session,
    currentUser: Users
) :

    newRecipe = Recipes(
        title = data.title,
        duration = data.duration,
        nbPersons = data.nbPersons,
        ownerId = currentUser.id
    )

    db.add(newRecipe)
    db.commit()
    db.refresh(newRecipe)

    return {
        "message": "Recipe created successfully.",
        "recipe": newRecipe
    }



def updateRecipe(
    id: int, 
    patch: PatchRecipe,
    db: Session,
    currentUser: Users
) :
    
    recipe = db.query(Recipes).filter(Recipes.id == id).first()
    if recipe is None :
        raise HTTPException(
            status_code=404,
            detail="No recipe with this id."
        )

    isOwner = recipe.ownerId == currentUser.id
    if not isOwner :
        raise HTTPException(
            status_code=403,
            detail="Can't patch another one's recipe."
        )

    if patch.title : recipe.title = patch.title
    if patch.duration : recipe.duration = patch.duration
    if patch.nbPersons : recipe.nbPersons = patch.nbPersons

    db.commit()
    db.refresh(recipe)

    return {
        "message": "Recipe patched successfully.",
        "recipe": recipe
    }


def deleteRecipeById(
    id: int,
    db: Session,
    currentUser: Users
) :

    recipe = db.query(Recipes).filter(Recipes.id == id).first()
    if recipe is None :
        raise HTTPException(
            status_code=404,
            detail="No recipe with this id."
        )

    isOwner = recipe.ownerId == currentUser.id

    if not isOwner :
        raise HTTPException(
            status_code=403,
            detail="Can't delete another one's recipe."
        )

    db.delete(recipe)
    db.commit()

    return {
        "message": "Recipe deleted successfully."
    }
    