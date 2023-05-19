from src.models.models import *
from src.models.constants import *
from src.services.utils import Utils
from src.services.discord import DiscordManager
import time
from copy import copy

class Midjourney:
    def __init__(self, discord: DiscordManager, channel_id):
        self.discord = discord
        self.raw_payload = RawPayload(
            application_id=MidjourneyConstants.APPLICATION_ID,
            session_id=MidjourneyConstants.SESSION_ID,
            guild_id=DiscordConstants.GUILD_ID,
            channel_id=channel_id,
        )

    def imagine(self, prompt):
        option = Option(type=3, name='prompt', value=prompt)
        raw_payload = copy(self.raw_payload)
        raw_payload.id = MidjourneyConstants.IMAGINE_COMMAND_ID
        raw_payload.version = MidjourneyConstants.IMAGINE_COMMAND_VERSION
        raw_payload.name = MidjourneyConstants.IMAGINE_NAME
        raw_payload.description = MidjourneyConstants.IMAGINE_DESCRIPTION

        payload = Utils.BuildPayload(raw_payload, option)

        self.discord.interact(payload)

    def help(self):
        raw_payload = copy(self.raw_payload)
        raw_payload.id = MidjourneyConstants.HELP_COMMAND_ID
        raw_payload.version = MidjourneyConstants.HELP_COMMAND_VERSION
        raw_payload.name = MidjourneyConstants.HELP_NAME
        raw_payload.description = MidjourneyConstants.HELP_DESCRIPTION

        payload = Utils.BuildPayload(raw_payload)

        self.discord.interact(payload)

    def info(self):
        raw_payload = copy(self.raw_payload)
        raw_payload.id = MidjourneyConstants.INFO_COMMAND_ID
        raw_payload.version = MidjourneyConstants.INFO_COMMAND_VERSION
        raw_payload.name = MidjourneyConstants.INFO_NAME
        raw_payload.description = MidjourneyConstants.INFO_DESCRIPTION

        payload = Utils.BuildPayload(raw_payload)

        self.discord.interact(payload)

    def first_where(self, array, key, value=None):
        for item in array:
            if callable(key) and key(item):
                return item
            elif isinstance(key, str) and item.get(key, '').startswith(value):
                return item
        return None

    def get_imagine(self, prompt):
        response = self.client.get(f'{self.API_URL}/channels/{self.channel_id}/messages')
        response.raise_for_status()
        response_data = response.json()
        raw_message = self.first_where(response_data, lambda item: item['content'].startswith(f'**{prompt}** - <@{self.user_id}>') and not '%' in item['content'] and item['content'].endswith('(fast)'))
        if raw_message is None:
            return None
        return {
            'id': raw_message['id'],
            'prompt': prompt,
            'raw_message': raw_message
        }

    def upscale(self, message, upscale_index=0):
        if not hasattr(message, 'raw_message'):
            raise Exception('Upscale requires a message object obtained from the imagine/getImagine methods.')
        if upscale_index < 0 or upscale_index > 3:
            raise Exception('Upscale index must be between 0 and 3.')
        upscale_hash = None
        raw_message = message.raw_message
        if hasattr(raw_message, 'components') and isinstance(raw_message.components, list):
            upscales = raw_message.components[0].components
            upscale_hash = upscales[upscale_index].custom_id
        option = Option(type=3, name='upscale', value=str(upscale_index))
        app_cmd = ApplicationCommand(
            id=self.DATA['upscale']['ID'],
            application_id=self.APPLICATION_ID,
            version=self.DATA['upscale']['VERSION'],
            default_permission=True,
            default_member_permissions='',
            type=1,
            nsfw=False,
            name='upscale',
            description='Upscale an image using Midjourney AI',
            dm_permission=True,
            options=[option]
        )
        data = Data(
            version=self.DATA['upscale']['VERSION'],
            id=self.DATA['upscale']['ID'],
            name='upscale',
            type=1,
            options=[option],
            application_command=app_cmd,
            attachments=[]
        )
        payload = Payload(
            type=2,
            application_id=self.APPLICATION_ID,
            guild_id=self.guild_id,
            channel_id=self.channel_id,
            session_id=self.SESSION_ID,
            data=data
        )
        params = payload.to_dict()
        params['message_id'] = message.id
        self.client.post(f'{self.API_URL}/interactions', json=params)
        upscaled_photo_url = None
        while upscaled_photo_url is None:
            upscaled_photo_url = self.get_upscale(message, upscale_index)
            if upscaled_photo_url is None:
                time.sleep(3)
        return upscaled_photo_url

    def get_upscale(self, message, upscale_index=0):
        if not hasattr(message, 'raw_message'):
            raise Exception('Upscale requires a message object obtained from the imagine/getImagine methods.')
        if upscale_index < 0 or upscale_index > 3:
            raise Exception('Upscale index must be between 0 and 3.')
        prompt = message.prompt
        response = self.client.get(f'{self.API_URL}/channels/{self.channel_id}/messages')
        response.raise_for_status()
        response_data = response.json()
        message_index = upscale_index + 1
        message_content = f'**{prompt}** - Image #{message_index} <@{self.user_id}>'
        if upscale_index == 0:
            message_content = f'**{prompt}** - Original Image <@{self.user_id}>'
        message = self.first_where(response_data, lambda item: item['content'] == message_content or item['content'] == f'**{prompt}** - Upscaled by <@{self.user_id}> (fast)')
        if message is None:
            return None
        if hasattr(message, 'attachments') and isinstance(message.attachments, list):
            attachment = message.attachments[0]
            return attachment.url
        return None

    def generate(self, prompt, upscale_index=0):
        imagine = self.get_imagine(prompt)
        upscaled_photo_url = self.upscale(imagine, upscale_index)
        return {
            'imagine_message_id': imagine['id'],
            'upscaled_photo_url': upscaled_photo_url
        }
