# Standard Library
import datetime
import uuid
from typing import Optional

# Third-party
from sqlalchemy import Column, ForeignKey, text, types

# Sematic
from sematic.db.models.base import Base
from sematic.db.models.mixins.json_encodable_mixin import JSONEncodableMixin


class Edge(Base, JSONEncodableMixin):

    __tablename__ = "edges"

    id: str = Column(types.String(), primary_key=True, default=lambda: uuid.uuid4().hex)

    # Edge endpoints
    source_run_id: Optional[str] = Column(
        types.String(), ForeignKey("runs.id"), nullable=True, index=True
    )
    source_name: Optional[str] = Column(types.String(), nullable=True)
    destination_run_id: Optional[str] = Column(
        types.String(), ForeignKey("runs.id"), nullable=True, index=True
    )
    destination_name: Optional[str] = Column(types.String(), nullable=True)

    # Artifact
    artifact_id: Optional[str] = Column(
        types.String(), ForeignKey("artifacts.id"), nullable=True
    )

    parent_id: Optional[str] = Column(
        types.String(), ForeignKey("edges.id"), nullable=True
    )

    # Lifecycle timestamps
    created_at: datetime.datetime = Column(
        types.DateTime(), nullable=False, server_default=text('NOW()')
    )
    updated_at: datetime.datetime = Column(
        types.DateTime(),
        nullable=False,
        server_default=text('NOW()'),
        server_onupdate=text('NOW()'),
    )

    _EQUALITY_FIELDS = (
        "source_run_id",
        "source_name",
        "destination_run_id",
        "destination_name",
        "artifact_id",
        "parent_id",
    )

    # Necessary for testing purposes, see test_local_resolver.py
    def __eq__(self, other) -> bool:
        return all(
            getattr(self, field) == getattr(other, field)
            for field in self._EQUALITY_FIELDS
        )

    def __hash__(self) -> int:
        return hash(
            ":".join(
                map(str, [getattr(self, field) for field in self._EQUALITY_FIELDS])
            )
        )

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{field}={getattr(self, field)}"
            for field in (
                "id",
                "source_run_id",
                "destination_run_id",
                "destination_name",
                "artifact_id",
                "parent_id",
            )
        )
        return f"Edge({fields})"
