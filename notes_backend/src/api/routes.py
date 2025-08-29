"""
API route definitions for the Notes service with CRUD operations.
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from .db import get_db
from .schemas import NoteCreate, NoteOut, NoteUpdate
from .service import NoteService

router = APIRouter(prefix="/notes", tags=["Notes"])


def _service(db: Session = Depends(get_db)) -> NoteService:
    return NoteService(db)


@router.get(
    "",
    summary="List notes",
    description="Retrieve a list of all notes ordered by most recently created.",
    response_model=List[NoteOut],
    status_code=status.HTTP_200_OK,
)
def list_notes(svc: NoteService = Depends(_service)) -> List[NoteOut]:
    """
    List all notes.

    Returns:
    - 200 OK with an array of notes.
    """
    return svc.list_notes()


@router.post(
    "",
    summary="Create note",
    description="Create a new note with a title and content.",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
)
def create_note(payload: NoteCreate, svc: NoteService = Depends(_service)) -> NoteOut:
    """
    Create a note.

    Body:
    - title: string (1..255)
    - content: string (non-empty)

    Returns:
    - 201 Created with created note.
    """
    return svc.create_note(payload)


@router.get(
    "/{note_id}",
    summary="Get note",
    description="Get a single note by its ID.",
    response_model=NoteOut,
    status_code=status.HTTP_200_OK,
)
def get_note(note_id: int, svc: NoteService = Depends(_service)) -> NoteOut:
    """
    Get a note by ID.

    Path:
    - note_id: integer

    Returns:
    - 200 OK with the note, or 404 if not found.
    """
    return svc.get_note(note_id)


@router.put(
    "/{note_id}",
    summary="Update note",
    description="Update fields of a note. Provide at least one field.",
    response_model=NoteOut,
    status_code=status.HTTP_200_OK,
)
def update_note(note_id: int, payload: NoteUpdate, svc: NoteService = Depends(_service)) -> NoteOut:
    """
    Update a note by ID.

    Path:
    - note_id: integer

    Body (any of):
    - title: string (1..255)
    - content: string (non-empty)

    Returns:
    - 200 OK with updated note, 404 if not found, or 422 for invalid body.
    """
    return svc.update_note(note_id, payload)


@router.delete(
    "/{note_id}",
    summary="Delete note",
    description="Delete a note by its ID.",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_note(note_id: int, svc: NoteService = Depends(_service)) -> Response:
    """
    Delete a note.

    Path:
    - note_id: integer

    Returns:
    - 204 No Content on success, or 404 if not found.
    """
    svc.delete_note(note_id)
    # Explicitly return a 204 No Content with no response body
    return Response(status_code=status.HTTP_204_NO_CONTENT)
