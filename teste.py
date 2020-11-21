import requests


from serialize import serialize

resp = requests.get(f"https://rawg.io/api/games/the-witcher-3-wild-hunt")
data = resp.json()


for d in data['stores']:
    print(d['store']['name'])


    