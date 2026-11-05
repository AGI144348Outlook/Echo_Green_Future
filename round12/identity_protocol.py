"""Round 12: bounded self/other identity protocol. Synthetic identity only.

A registered actor identity is immutable for the life of this adapter. Roles
are contextual, not permissions. This module does not grant database access.
"""
from dataclasses import dataclass, field
from typing import Mapping
import json

MAX_PAYLOAD = 2048

@dataclass(frozen=True)
class Actor:
    actor_id: str
    display_name: str

@dataclass(frozen=True)
class Envelope:
    sender: str
    recipient: str
    context: str
    payload: str
    source_ref: str
    claimed_sender: str

@dataclass
class IdentityProtocol:
    actors: dict[str, Actor] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)

    def register(self, actor_id: str, display_name: str) -> Actor:
        if not actor_id or not display_name:
            raise ValueError("identity fields required")
        if actor_id in self.actors:
            raise ValueError("identity already registered")
        actor = Actor(actor_id, display_name)
        self.actors[actor_id] = actor
        return actor

    def identify(self, observer: str, subject: str) -> dict:
        if observer not in self.actors:
            raise ValueError("unknown observer")
        if subject not in self.actors:
            return {"relation": "unknown", "subject": subject, "evidence": "registry_absent"}
        return {"relation": "self" if observer == subject else "other",
                "subject": subject, "evidence": "registered_identity"}

    def send(self, envelope: Envelope, authenticated_actor: str) -> dict:
        if envelope.sender not in self.actors or envelope.recipient not in self.actors:
            raise ValueError("unknown endpoint")
        if authenticated_actor != envelope.sender or envelope.claimed_sender != envelope.sender:
            raise PermissionError("sender authentication mismatch")
        if not envelope.context or not envelope.source_ref:
            raise ValueError("context and provenance required")
        if not isinstance(envelope.payload, str) or len(envelope.payload.encode("utf-8")) > MAX_PAYLOAD:
            raise ValueError("payload exceeds bound")
        event = {"sender": envelope.sender, "recipient": envelope.recipient,
                 "context": envelope.context, "payload": envelope.payload,
                 "source_ref": envelope.source_ref,
                 "sender_role": "source", "recipient_role": "recipient",
                 "claim_status": "unverified"}
        self.events.append(event)
        return dict(event)

    def transcript(self) -> str:
        return json.dumps(self.events, sort_keys=True, ensure_ascii=False)
