"""
Pydantic models (schemas) for the Notes API requests and responses.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Short title of the note")
    content: str = Field(..., min_length=1, description="Main text content of the note")

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title must not be empty or whitespace")
        return v

    @field_validator("content")
    @classmethod
    def strip_content(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Content must not be empty or whitespace")
        return v


class NoteCreate(NoteBase):
    """
    Schema for creating a note.
    """


class NoteUpdate(BaseModel):
    """
    Schema for updating a note. All fields are optional, but at least one must be provided.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated title")
    content: Optional[str] = Field(None, min_length=1, description="Updated content")

    @field_validator("title")
    @classmethod
    def strip_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Title must not be empty or whitespace")
        return v

    @field_validator("content")
    @classmethod
    def strip_content(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Content must not be empty or whitespace")
        return v


class NoteOut(BaseModel):
    id: int = Field(..., description="Unique identifier of the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(..., description="Content of the note")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")

    class Config:
        from_attributes = True
