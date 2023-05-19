from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Option:
    type: int
    name: str
    value: Optional[str] = None
    description: Optional[str] = None
    required: Optional[bool] = None

    def to_dict(self):
        option_dict = {
            'type': self.type,
            'name': self.name
        }
        if self.value is not None:
            option_dict['value'] = self.value
        if self.description is not None:
            option_dict['description'] = self.description
        if self.required is not None:
            option_dict['required'] = self.required
        return option_dict

@dataclass
class ApplicationCommand:
    id: str
    application_id: str
    version: str
    name: str
    description: str
    default_permission: Optional[bool] = None
    default_member_permissions: Optional[str] = None
    type: int = 1
    nsfw: bool = False
    dm_permission: bool = True
    options: Optional[List[Option]] = None
    contexts: Optional[List[str]] = None

    def to_dict(self):
        command_dict = {
            'id': self.id,
            'application_id': self.application_id,
            'version': self.version,
            'default_permission': self.default_permission,
            'default_member_permissions': self.default_member_permissions,
            'type': self.type,
            'nsfw': self.nsfw,
            'name': self.name,
            'description': self.description,
            'dm_permission': self.dm_permission
        }
        if self.options is not None:
            command_dict['options'] = [option.to_dict() for option in self.options]
        if self.contexts is not None:
            command_dict['contexts'] = self.contexts
        return command_dict

@dataclass
class Data:
    version: str
    id: str
    name: str
    type: int
    options: List[Option]
    application_command: ApplicationCommand
    attachments: List[str]

    def to_dict(self):
        return {
            'version': self.version,
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'options': [option.to_dict() for option in self.options],
            'application_command': self.application_command.to_dict(),
            'attachments': self.attachments
        }

@dataclass
class Payload:
    type: int
    application_id: str
    guild_id: Optional[str]
    channel_id: Optional[str]
    session_id: Optional[str]
    data: Data

    def to_dict(self):
        return {
            'type': self.type,
            'application_id': self.application_id,
            'guild_id': self.guild_id,
            'channel_id': self.channel_id,
            'session_id': self.session_id,
            'data': self.data.to_dict()
        }

@dataclass
class RawPayload:
    application_id: str
    guild_id: str
    channel_id: str
    session_id: str
    id: str = ''
    version: int = ''
    name: str = ''
    description: str = ''
