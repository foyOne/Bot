from datetime import datetime, date


def PrepareDate(dateValue):
    if dateValue in ['t', 'today']:
        return date.today()
    else:
        d = datetime.strptime(dateValue, '%d.%m.%Y').date()
        cmp = date.today()
        if d > cmp:
            raise Exception('Date is greater than current')
        return d

def ParseData(data: list):
    try:
        data[0] = PrepareDate(data[0])
        data[1] = ' '.join(data[1].split())
        data[2] = int(data[2])
        data[3] = int(data[3])
        data[4] = data[4] or 0
    except:
        return False
    return True
# def GetUpdatesJson():
#     params = {
#         'timeout': 100,
#         'offset': None
#     }
#     response = requests.get(Settings.BotURL + 'getUpdates', data=params)
#     return response.json()

# def LastUpdate(response):
#     results = response['result']
#     return results[-1]


# def GetChatId(result):
#     return result['message']['chat']['id']

# def SendMessage(chatId, message):
#     params = {
#         'chat_id': chatId,
#         'text': message
#     }
#     return requests.post(Settings.BotURL + 'sendMessage', data=params)



# def main():
#     a = os.path.isfile('d.sqlite3')
#     print(a)

# if __name__ == '__main__':
#     main()