from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    new_contact = await repository_contacts.create_contact(body, current_user, db)
    return new_contact


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(limit: int = Query(10, le=300), offset: int = 0,
                       current_user: User = Depends(auth_service.get_current_user),
                       db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact_by_id(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                            db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), current_user: User = Depends(auth_service.get_current_user),
                         db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.get("/search/", response_model=List[ContactResponse])
async def search_contacts(query: str, current_user: User = Depends(auth_service.get_current_user),
                          db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(query, current_user, db)
    return contacts


@router.get("/upcoming-birthdays/", response_model=List[ContactResponse])
async def get_contacts_birthdays(current_user: User = Depends(auth_service.get_current_user),
                                 db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_birthdays(current_user, db)
    return contacts
