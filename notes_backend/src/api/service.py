"""
Service layer for Note business logic.
"""
from __future__ import annotations

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .repository import NoteRepository
from .schemas import NoteCreate, NoteOut, NoteUpdate


class NoteService:
    """
    Service encapsulating note business logic.
    """

    def __init__(self, db: Session):
        self.repo = NoteRepository(db)

    # PUBLIC_INTERFACE
    def list_notes(self) -> List[NoteOut]:
        """Return all notes ordered by creation date descending."""
        notes = self.repo.list()
        return [NoteOut.model_validate(n) for n in notes]

    # PUBLIC_INTERFACE
    def get_note(self, note_id: int) -> NoteOut:
        """Return a single note or 404."""
        note = self.repo.get(note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return NoteOut.model_validate(note)

    # PUBLIC_INTERFACE
    def create_note(self, payload: NoteCreate) -> NoteOut:
        """Create a new note."""
        note = self.repo.create(payload)
        return NoteOut.model_validate(note)

    # PUBLIC_INTERFACE
    def update_note(self, note_id: int, payload: NoteUpdate) -> NoteOut:
        """Update a note, requiring at least one field to be provided."""
        if payload.title is None and payload.content is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="At least one of 'title' or 'content' must be provided",
            )
        note = self.repo.get(note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        updated = self.repo.update(note, payload)
        return NoteOut.model_validate(updated)

    # PUBLIC_INTERFACE
    def delete_note(self, note_id: int) -> None:
        """Delete a note by ID or 404."""
        note = self.repo.get(note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        self.repo.delete(note)
