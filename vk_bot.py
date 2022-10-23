from random import randrange
import requests
from vk_api.utils import get_random_id
from vk_users_search import *
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload

with open('app_token.txt', 'r') as f:
    token = f.read()

vv = VK(TOKEN)


attachments = []
session = requests.Session()
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
upload = VkUpload(vk_session)

photo_found = vv.get_best_photos()
user_info = vv.get_info_by_user_id()

link = photo_found[24128099][0]['link']

image = session.get(link, stream=True)
photo = upload.photo_messages(photos=image.raw)[0]
attachments.append(
    'photo{}_{}'.format(photo['owner_id'], photo['id']))
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
    #Слушаем longpoll, если пришло сообщение то:
        if event.text == 'привет' or event.text == 'Привет': #Если написали заданную фразу
            if event.from_user: #Если написали в ЛС
                vk.messages.send( #Отправляем сообщение
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    attachment=','.join(attachments),
                    message=f'{user_info}')
            elif event.from_chat: #Если написали в Беседе
                vk.messages.send( #Отправляем собщение
                    chat_id=event.chat_id,
                    random_id=get_random_id(),
                    attachment=','.join(attachments),
                    message='hey')
