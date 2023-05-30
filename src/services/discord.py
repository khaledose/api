from typing import Optional
from src.models.constants import DiscordConstants
import requests

class DiscordManager:
    def __init__(self, oauth_token) -> None:
        self.oauth_token = oauth_token
        self.client = requests.Session()
        self.client.headers.update({'Authorization': self.oauth_token})

    def get_server(self) -> Optional[str]:
        response = self.client.get(f'{DiscordConstants.API_URL}/users/@me/guilds')
        response.raise_for_status()
        guilds = response.json()
        for guild in guilds:
            if isinstance(guild, dict) and guild['owner']:
                return guild['id']
        return None

    def create_channel(self, user: str, guild_id: str) -> Optional[str]:
        response = self.client.get(f'{DiscordConstants.API_URL}/guilds/{guild_id}/channels')
        response.raise_for_status()
        channels = response.json()
        for channel in channels:
            if isinstance(channel, dict) and channel.get('name', None) == user:
                return channel.get('id', None)
        payload = {
            'name': user,
            'type': 0,
        }
        response = self.client.post(f'{DiscordConstants.API_URL}/guilds/{guild_id}/channels', json=payload)
        response.raise_for_status()
        channel = response.json()
        return channel.get('id', None)

    def clean_channel(self, channel_id: str) -> None:
        response = self.client.get(f'{DiscordConstants.API_URL}/channels/{channel_id}/messages')
        response.raise_for_status()
        messages = response.json()
        for msg in messages:
            id = msg['id']
            self.client.delete(f'{DiscordConstants.API_URL}/channels/{channel_id}/messages/{id}')

    def interact(self, payload) -> None:
        response = self.client.post(f'{DiscordConstants.API_URL}/interactions', json=payload.to_dict())
        response.raise_for_status()