import json

payload = {
    'system': 'C:/Users/huangtingwei/Desktop/飞行器pythonProject17/'
}
with open('system.json','w') as f:
    json.dump(payload, f)

with open("system.json", "r") as f:
    dict = json.load(f)
    print(dict['system'])