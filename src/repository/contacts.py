from typing import List
from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.sql import extract
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel


async def create_contact(body: ContactModel,  current_user: User, db: Session):
    new_contact = Contact(**body.dict(), user_id=current_user.id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def get_contacts(limit: int, offset: int, current_user: User, db: Session):
    contacts = db.query(Contact).filter(and_(Contact.user_id == current_user.id)).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, current_user: User, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id, user_id=current_user.id).first()
    return contact


async def update_contact(body: ContactModel, contact_id: int, current_user: User, db: Session):
    contact = await get_contact_by_id(contact_id, current_user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        db.commit()
    return contact


async def remove_contact(contact_id: int, current_user: User, db: Session):
    contact = await get_contact_by_id(contact_id, current_user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(query: str, current_user: User, db: Session):
    contacts = db.query(Contact).filter(
        and_(Contact.user_id == current_user.id),
        Contact.first_name.ilike(f"%{query}%") |
        Contact.last_name.ilike(f"%{query}%") |
        Contact.email.ilike(f"%{query}%")
    ).all()
    return contacts


async def get_contacts_birthdays(current_user: User, db: Session):
    today_month = datetime.today().month
    today_day = datetime.today().day
    future_date_month = (datetime.today() + timedelta(days=7)).month
    future_date_day = (datetime.today() + timedelta(days=7)).day

    contacts = db.query(Contact).filter(and_(
        Contact.user_id == current_user.id),
        (extract('month', Contact.birth_date) == today_month) & (extract('day', Contact.birth_date) >= today_day) |
        (extract('month', Contact.birth_date) == future_date_month) & (extract('day', Contact.birth_date) <= future_date_day)
    ).all()
    return contacts













