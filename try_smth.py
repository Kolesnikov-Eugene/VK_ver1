a = {1: [{'likes':5, 'link':'link'}, {'likes':7, 'link':'link'}],
     2: [{'likes':5, 'link':'link'}, {'likes':9, 'link':'link'}],
     3: [{'likes':3, 'link':'link'}, {'likes':6, 'link':'link'}]
     }

new_dict = dict()
for item in a.items():

     sorted_a = sorted(item[1], key=lambda x: x['likes'], reverse=True)
     new_dict[item[0]] = sorted_a

print(new_dict)