
import requests
import time

MaxPrice,MinPrice = '0','0'

Cookie = open('ROBLOSECURITY.txt').read()


def GetIds():
  Ids = []
  Request = requests.get(f'https://catalog.roblox.com/v1/search/items?category=All&creatorTargetId=1&cursor=1_2_38d43aaad573938654a22a6ae8524251&limit=60&maxPrice={MaxPrice}&minPrice={MinPrice}').json()
  for Asset in Request["data"]:
    id = Asset['id']
    try:
      if Asset['itemType'] == 'Asset':
        pid = requests.get(f'https://api.roblox.com/marketplace/productinfo?assetId={id}').json()
        print(id)
        p = pid['ProductId']
      else:
        pid = requests.get(f'https://catalog.roblox.com/v1/bundles/{id}/details').json()
        p = pid['product']['id']
    except:
      print('waiting 60')
      time.sleep(60)
      if Asset['itemType'] == 'Asset':
        pid = requests.get(f'https://api.roblox.com/marketplace/productinfo?assetId={id}').json()
        print(id)
        p = pid['ProductId']
      else:
        pid = requests.get(f'https://catalog.roblox.com/v1/bundles/{id}/details').json()
        p = pid['product']['id']
    Ids.append(p)
  Cursor = Request["nextPageCursor"]
  while Cursor:
    Request = requests.get(f'https://catalog.roblox.com/v1/search/items?category=All&creatorTargetId=1&cursor={Cursor}&limit=60&maxPrice={MaxPrice}&minPrice={MinPrice}').json()
    for Asset in Request["data"]:
      id = Asset['id']
      try:
        if Asset['itemType'] == 'Asset':
          pid = requests.get(f'https://api.roblox.com/marketplace/productinfo?assetId={id}').json()
          print(id)
          p = pid['ProductId']
        else:
          pid = requests.get(f'https://catalog.roblox.com/v1/bundles/{id}/details').json()
          p = pid['product']['id']
      except:
        print('waiting 60')
        time.sleep(60)
        if Asset['itemType'] == 'Asset':
          pid = requests.get(f'https://api.roblox.com/marketplace/productinfo?assetId={id}').json()
          print(id)
          p = pid['ProductId']
        else:
          pid = requests.get(f'https://catalog.roblox.com/v1/bundles/{id}/details').json()
          p = pid['product']['id']
      Ids.append(p)
    Cursor = Request["nextPageCursor"] or None
  return Ids
  

session = requests.Session()
session.cookies['.ROBLOSECURITY'] = Cookie
try:
  Info = session.get('http://www.roblox.com/mobileapi/userinfo').json()
  xc = session.post("https://auth.roblox.com/v2/logout").headers['X-CSRF-TOKEN']
  print('Logged in as '+Info['UserName'])
except:
  print('Invalid Cookie')
  exit()

Ids = GetIds()


for Asset in Ids:
  post = session.post(f'https://economy.roblox.com/v1/purchases/products/{Asset}', data={'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': 1} ,headers={"X-CSRF-TOKEN": xc})
  print(f'Bought item {Asset}')
  if 'TooManyRequests' in post.text:
    print('Too many requests, waiting 60 sec')
    for i in range(60):
      print(60-i)
      time.sleep(1)
    post = session.post(f'https://economy.roblox.com/v1/purchases/products/{Asset}', data={'expectedCurrency': 1, 'expectedPrice': 0, 'expectedSellerId': 1} ,headers={"X-CSRF-TOKEN": xc})

print('Done!')