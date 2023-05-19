from src.models.models import *

class Utils:
    @staticmethod
    def BuildPayload(raw: RawPayload, options: Option = None, attachments: list = None):
        app_cmd = ApplicationCommand(
                id=raw.id,
                application_id=raw.application_id,
                version=raw.version,
                default_member_permissions=None,
                type=1,
                nsfw=False,
                name=raw.name,
                description=raw.description,
                dm_permission=True,
                contexts=None,
                options=[options] if options is not None else []
            )
        
        data = Data(
            version=raw.version,
            id=raw.id,
            name=raw.name,
            type=1,
            options=[options] if options is not None else [],
            application_command=app_cmd,
            attachments=[attachments] if attachments is not None else []
        )
        
        payload = Payload(
            type=2,
            application_id=raw.application_id,
            guild_id=raw.guild_id,
            channel_id=raw.channel_id,
            session_id=raw.session_id,
            data=data
        )
        
        return payload