from src.services.midjourney import Midjourney
from src.services.discord import DiscordManager
from src.services.auth import FirebaseUserManager


# # mj.imagine('a cat flying in a cloudy sky wearing superhero suit')
# mj.help()
# 

firebase = FirebaseUserManager('./secretKey.json')

# firebase.create_user('email@gmail.com', '123ASD@!#')

user = firebase.get_user_by_email('email@gmail.com')
print(user.uid)

# dm = DiscordManager(oauth_token=prod_oath)
# channel_id = dm.create_channel('user1')

# mj = Midjourney(dm, channel_id)
# mj.help()
# mj.info()
# mj.imagine('a cat flying in a cloudy sky wearing superhero suit')