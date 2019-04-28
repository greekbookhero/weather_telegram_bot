import requests
import misc
import json
token = misc.token
URL = 'https://api.telegram.org/bot' + token + '/'
pogoda_URL='http://api.openweathermap.org/data/2.5/weather?q='
global last_update_id
last_update_id=0
def get_updates():
        url = URL+"getupdates"
        r = requests.get(url)
        return r.json()

def get_city_id(s_city_name):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
            params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': misc.API})
            data = res.json()
            city_id=data['list'][0]['id']
            return city_id

        except Exception as e:
            return " "

def get_pogoda(city):
    if city==" ":
        return "Попробуйте ввести на английском языке или проверь правописание"
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                 params={'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': misc.API})
    data=res.json()
    temp=data['main']['temp']
    humidity=data['main']['humidity']
    maxtemp=data['main']['temp_max']
    mintemp=data['main']['temp_min']
    if int(maxtemp)>0:
        maxtemp="＋"+str(maxtemp)
    if int(mintemp)>0:
        mintemp="＋"+str(mintemp)
    if int(temp)>0:
        return str("Погода на данный момент"+' ＋'+str(temp)+"°C"+"\n"+"Погода на улице "+str(data['weather'][0]['description']+"\n"+"Максимальная возможная температура  "+str(maxtemp)+"\n"+"Минимально возможная температура  "+str(mintemp)+"\n"+"Влажность воздуха "+str(humidity)+"%"))
    else:
        return str("Погода на данный момент"+str(temp)+"°C"+"\n"+"Погода на улице "+str(data['weather'][0]['description']+"\n"+"Максимальная возможная температура  "+str(maxtemp)+"\n"+"Минимально возможная температура  "+str(mintemp)+"\n"+"Влажность воздуха "+str(humidity)+"%"))

def get_message():
    data = get_updates()
    last_object = data['result'][-1]
    current_update_id = last_object['update_id']
    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id = last_object['message']['chat']['id']
        message_text=last_object['message']['text']
        message = {'text':message_text,'chat_id':chat_id}
        return message
    return None

def send_message(chat_id,text):
    url=URL+'sendmessage?chat_id={}&text={}'.format(chat_id,text)
    requests.get(url)

def main():
        answer=get_message()
        while True:
            answer=get_message()
            if answer != None:
                chat_id=answer['chat_id']
                text =answer['text']
                text=text.lower()
                uin=get_city_id(text)
                send_message(chat_id,get_pogoda(uin))
                if text=='/start':
                    send_message(chat_id,'Здравствуйте! Я могу показать погоду любого города . Напишите название города, который вам нужен, пожалуйста.')
            else:
                continue

if __name__== '__main__':
      main()
