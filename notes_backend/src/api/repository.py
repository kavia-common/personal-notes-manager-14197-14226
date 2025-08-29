"""
Repository layer for Note persistence operations.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import NoteORM
from .schemas import NoteCreate, NoteUpdate


class NoteRepository:
    """
    Repository providing CRUD operations for notes.
    """

    def __init__(self, db: Session):
        self.db = db

    def list(self) -> List[NoteORM]:
        stmt = select(NoteORM).order_by(NoteORM.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get(self, note_id: int) -> Optional[NoteORM]:
        return self.db.get(NoteORM, note_id)

    def create(self, payload: NoteCreate) -> NoteORM:
        note = NoteORM(title=payload.title, content=payload.content)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def update(self, note: NoteORM, payload: NoteUpdate) -> NoteORM:
        if payload.title is not None:
            note.title = payload.title
        if payload.content is not None:
            note.content = payload.content
        note.touch()
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def delete(self, note: NoteORM) -> None:
        self.db.delete(note)
        self.db.commit()
