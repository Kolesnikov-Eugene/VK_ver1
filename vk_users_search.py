import requests
import vk_api
from vk_api import VkTools
from pprint import pprint
import json

URL = 'https://vk.com/id'
with open('token.txt', 'r') as f:
    TOKEN = f.read()


class VK:
    def __init__(self, token):
        # self.user_id = user_id
        self.token = token

    def get_profile_info(self):
        vk_session = vk_api.VkApi(app_id=6326581, token=self.token)
        self.vk = vk_session.get_api()
        response = self.vk.account.getProfileInfo()
        user_info = self.vk.users.get(user_id='6326581', fields='interests, music')
        print(response)
        year_of_birth = int(response['bdate'].split('.')[-1])  # get year of birth
        self.self_age = 2022 - year_of_birth  # get age
        # print(self.self_age)
        # print(user_info)
        self.hometown = str(response['home_town'])
        self.gender = str(response['sex'])
        self.birth_date = str(response['bdate'])
        interests = set(user_info[0]['interests'])
        # print(interests)
        # print(self.gender, self.hometown, self.birth_date)
        return self.vk, self.hometown, self.gender, self.birth_date, response, user_info, interests, self.self_age

    def find_people(self):
        self.get_profile_info()
        gender_match = None
        if self.gender == '1':
            gender_match = '2'
        elif self.gender == '2':
            gender_match = '1'

        age_min = str(self.self_age - 3)  # min age for search matches
        age_max = str(self.self_age + 3)  # max age for search matches
        common_interests = set()
        photos = {}
        self.list_of_ids = []

        matches = self.vk.users.search(count='5', hometown=self.hometown, sex=gender_match, age_from=age_min, age_to=age_max,
                                       fields='interests, bdate, about, activities')
        for user in matches['items']:
            self.list_of_ids.append(user['id'])
        return self.list_of_ids

    def get_photos(self):
        self.find_people()
        self.photos_dict = dict()
        for id in self.list_of_ids:
            self.photos_dict[id] = []
            try:
                p = self.vk.photos.get(owner_id=id, album_id='profile', extended='1', photo_sizes='1')
                for n in range(p['count']):
                    try:
                        self.photos_dict[id].append({'likes': p['items'][n]['likes']['count'],
                                                     'link': p['items'][n]['sizes'][0]['url']})
                    except IndexError as err:
                        print('no')
            except vk_api.exceptions.ApiError as err:
                print('no access')
        return self.photos_dict

    def get_best_photos(self):
        self.get_photos()
        sorted_dict_of_photos = dict()
        for item in self.photos_dict.items():
            sorted_tuple = sorted(item[1], key=lambda x: x['likes'], reverse=True)
            sorted_dict_of_photos[item[0]] = sorted_tuple
        return sorted_dict_of_photos

    def get_info_by_user_id(self):
        for match_id in self.list_of_ids:
            info = self.vk.users.get(user_id=match_id)
            yield info[0]['first_name'], info[0]['last_name'], f'link: {URL}{match_id}'
            break


if __name__ == '__main__':
    vv = VK(TOKEN)
    photo_found = vv.find_people()
    pprint(photo_found)
    af = vv.get_info_by_user_id()
    for name in af:
        print(name)
