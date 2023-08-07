from vkbottle.bot import BotLabeler, Message, rules
from vkbottle_types.objects import MessagesConversation
from typing import Optional
from file import file_editor
import random

chat_labeler = BotLabeler()
chat_labeler.vbml_ignore_case = True
chat_labeler.auto_rules = [rules.FromUserRule()]
file_edit = file_editor
    
data = file_editor.open_data("data.json")

async def get_user(chat_id, user_id, nickname = ""):
    chat_id = "chat"
    user_id = str(user_id)
    nickname = str(nickname)

    if chat_id not in data:
        data.update({chat_id: {}})

    if user_id not in data.get(chat_id):
        return nickname

    await file_editor.save_data(data, "data.json")
       
    return data.get(chat_id).get(user_id)


async def set_user(chat_id, user_id, nickname):
    chat_id = "chat"
    user_id = str(user_id)
    nickname = str(nickname)

    if chat_id not in data:
        data.update({chat_id: {}})

    data.get(chat_id).update({user_id: nickname})
    
    await file_editor.save_data(data, "data.json")


async def check_string(text):
    bad_symbol = ["/", "@", "[", "]", "\"", "\\", "\n", ":", "🪇"]

    for i in bad_symbol:
        if i in text:
            return False

    return True 

@chat_labeler.message(text="ники")
async def send_nickname_list(message: Message):
    users = await message.ctx_api.messages.get_conversation_members(peer_id=message.peer_id, fields="nickname")
    text = "📝Список ников беседы:\n\n"

    for user in users.profiles:
        if str(user.id) in data.get("chat"):
            text += f"[id{user.id}|{await get_user(message.peer_id, user.id)}] - {user.first_name + ' ' + user.last_name}\n"
    
    text += "\n💬 Чтобы установить себе ник, введите команду ник {Ваш_ник}"
    await message.answer(text, disable_mentions=1)



@chat_labeler.message(text=["ник <item>", "ник"])
async def send_callback_button(message: Message, item: Optional[str] = None):
    if item is None:
        await message.answer("💬 Чтобы установить себе ник, введите команду ник {Ваш_ник}")
    else:   
        item = item.strip()
        if await check_string(item):    
            if len(item) > 26:
                await message.answer("ник длиннее 26 символов")
                return
            if len(item) < 3:
                await message.answer("ник короче 3 символов")
                return
            else:
                await set_user(message.peer_id, message.from_id, item)
                await message.answer("ник изменен на " + item)
        else:
            await message.answer("Запретные символы в нике")


@chat_labeler.message(text="рандом")
async def send_callback_button(message: Message):
    users = await message.ctx_api.messages.get_conversation_members(peer_id=message.peer_id, fields="nickname")
    user = random.choice(users.profiles)
    await message.answer(f"💬 Рандомный участник: [id{user.id}|{await get_user(message.peer_id, user.id, user.first_name + ' ' + user.last_name)}]\n")


@chat_labeler.message(text="шипперим")
async def send_callback_button(message: Message):
    users = await message.ctx_api.messages.get_conversation_members(peer_id=message.peer_id, fields="nickname")
    user = random.choices(users.profiles, k=2)
    print(user[1].first_name + ' ' + user[1].last_name)
    await message.answer(f"💘 РАНДОМ ШИППЕРИМ: [id{user[0].id}|{await get_user(message.peer_id, user[0].id, user[0].first_name + ' ' + user[0].last_name)}]" +
                         f" + [id{user[1].id}|{await get_user(message.peer_id, user[1].id, user[1].first_name + ' ' + user[1].last_name)}]. Любите друг друга и берегите. Мур.")


@chat_labeler.message(text="бот погода")
async def send_callback_button(message: Message):
    weather = file_editor.open_data("weather.json")

    text = f"""
    🏙 Город: {random.choice(weather.get("city"))}
    🌏 Страна: {random.choice(weather.get("county"))}
    🌤️ Погода: {random.choice(weather.get("weather"))}
    🌡 Температура: {random.randint(-60, 60)}°C
    💨 Ветер: {random.choice(weather.get("wind"))}
    📅 Сегодня {random.randint(1, 31)} {random.choice(weather.get("month"))} {random.randint(2000, 2100)} года
    {random.choice(weather.get("phrase"))}
    """

    await message.answer(text)