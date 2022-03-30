# -*- coding: utf-8 -*-
from cgi import test
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randint
from db import UsersInfo as user
import time

def sender(kayb,user_id,vk,text):
    if kayb == 1:
        keyboard = VkKeyboard(one_time = False, inline = False)
        keyboard.add_button(label = 'Cтатус', color = VkKeyboardColor.PRIMARY)
    vk.messages.send(user_id = user_id,random_id = get_random_id(),keyboard = keyboard.get_keyboard(),message = text)

  
def command(text,user_id,vk):
    print(text)
    if text.lower() == "статус" or text == "Cтатус":
        q = user.is_vip(user_id)
        if q == False:
            q = "VIP не куплена"
        else:
            q = f"VIP действует до {user.get_vip(user_id)}"
        data = vk.users.get(user_ids = user_id)
        name = data[0]["first_name"]
        cash = user.get_cash(user_id)
        sender(1,user_id,vk,f"[id{user_id}|{name}] {user.get_role(user_id)}\nБаланс {cash}\nid:{user_id}\n{q}\nС нами с {user.get_reg(user_id)}")
    
    elif "give-vip" in text:
        listt = str(text).split()
        screen_name = listt[1].split('/')[-1]
        data = vk.users.get(user_ids=screen_name )
        give_id = data[0]["id"]
        if user.get_role(user_id) == "Admin" or user.get_role(user_id) == "Admin+" and user.is_reg(give_id) == True:
            user.give_vip(user_id,listt[2])
            name = data[0]["first_name"]
            sender(1,user_id,vk,f"[id{give_id}|{name}] теперь VIP до {user.get_vip(give_id)}")

    elif "give-admin" in text:
        listt = str(text).split()
        data = vk.users.get(user_ids=screen_name )
        give_id = data[0]["id"]
        if user.get_role(user_id) == "Admin+" and user.is_reg(give_id) == True:
            screen_name = listt[1].split('/')[-1]
            name = data[0]["first_name"]
            cash = user.get_cash(give_id)
            q = user.is_vip(user_id)
            if q == False:
                q = "VIP не куплена"
            else:
                q = f"VIP действует до {user.get_vip(user_id)}"
            if user_id != give_id:
                user.give_admin(give_id,user_id)
                sender(1,user_id,vk,f"[id{give_id}|{name}] {user.get_role(give_id)}\nБаланс {cash}\nid:{give_id}\n{q}\nС нами с {user.get_reg(give_id)}")
            else:
                data = vk.users.get(user_ids=user_id )
                name = data[0]["first_name"]
                sender(1,user_id,vk,f"[id{user_id}|{name}] вы не можете себя понизить с Admin+ до Admin")
    

def main():
    vk_session = vk_api.VkApi(token='')

    longpoll = VkBotLongPoll(vk_session, '')

    vk = vk_session.get_api()

    try:
        for event in longpoll.listen(): 
            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.obj.text
                user_id = event.obj.from_id
                if event.obj.peer_id < 2000000000:
                    if user.is_reg(user_id) == False:
                        if text.lower() == "начать":
                            user.insert(user_id)
                            keyboard = VkKeyboard(one_time = False, inline = False)
                            keyboard.add_button(label = 'Чек вип', color = VkKeyboardColor.PRIMARY)
                            sender(1,user_id,vk,"Вы зарегистирировались в чат-игре Кликер 👍🏻\nКликайте на кнопку 'Клик' и зарабатывайте очки 💥\n\nДля просмотра топа игроков по кликам нажмите кнопку 'Топ игроков' 👥\n\nЕсли нужна помощь используйте команду 'помощь' 📣\n\nПриятной игры 😘")
                    else:
                        command(text,user_id,vk)
                        

    #except Exception as e:
    except TimeoutError:
            #print(f"--------------- [ {e} ] ---------------")
            print("Переподключение к серверам...")
            time.sleep(1) 
            main() 


                

if __name__ == '__main__':
    main()