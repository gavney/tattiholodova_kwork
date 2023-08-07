from vkbottle.bot import BotLabeler, Message, rules
from bot_config import vk_api, group_id
from typing import Optional
from file import file_editor
import random

roleplay_labeler = BotLabeler()
roleplay_labeler.vbml_ignore_case = True
file_edit = file_editor
    
async def get_user(chat_id, user_id, nickname):
    data = file_editor.open_data("data.json")
    chat_id = "chat"
    user_id = str(user_id)
    nickname = str(nickname)

    if chat_id not in data:
        data.update({chat_id: {}})

    if user_id not in data.get(chat_id):
        data.get(chat_id).update({user_id: nickname})

    await file_editor.save_data(data, "data.json")
       
    return data.get(chat_id).get(user_id)

async def get_attachments(attachments):
    result = []
    if attachments:
        print(len(attachments))
        for i in attachments:
            if i.photo:
                result.append(f"photo{i.photo.owner_id}_{i.photo.id}_{i.photo.access_key}")
            if i.audio:
                result.append(f"audio{i.audio.owner_id}_{i.audio.id}_{i.audio.access_key}")
            if i.video:
                result.append(f"video{i.video.owner_id}_{i.video.id}_{i.video.access_key}")
            if i.doc:
                result.append(f"doc{i.doc.owner_id}_{i.doc.id}_{i.doc.access_key}")
            if i.market:
                result.append(f"market{i.market.owner_id}_{i.market.id}_{i.market.access_key}")
            if i.poll:
                result.append(f"poll{i.poll.owner_id}_{i.poll.id}_{i.poll.access_key}")
    if len(result) == 0:
        result.append(" ")
    return result

roleplay_command = file_editor.open_data("roleplay.json")

@roleplay_labeler.message(rules.PeerRule(from_chat=False), text="команды")
async def send_callback_button(message: Message):
    text = "📝 Список команд:\n\n"
    for i in roleplay_command.keys():
        text += f"{i}\n"

    await message.answer(text)

@roleplay_labeler.message(text=["+рпо <item1>\n<item2>", "+рп <item1>\n<item2>", "+рп", "+рпо", "-рп <item1>"])
async def send_callback_button(message: Message, item1: Optional[str] = None,
                                item2: Optional[str] = None):
    
    if message.from_id in file_editor.open_data("config.json").get("admins"): 
        if item1 is None:
            await message.answer("+-рп <команда>\n<действие>")
        else:
            mes = await message.ctx_api.messages.get_by_id(cmids = message.conversation_message_id, peer_id = message.peer_id)

            item1 = item1.lower().strip()
            item2 = item1.strip()

            attachments = await get_attachments(mes.items[0].attachments)
            if message.text.split(" ")[0] == "+рп":
                roleplay_command.update({item1: [item2, False, attachments]})
                await message.answer("команда добавлена без ответа")
            
            elif message.text.split(" ")[0] == "-рп" and item1 in roleplay_command:
                roleplay_command.pop(item1)
                await message.answer("команда удалена")

            else:
                roleplay_command.update({item1.strip(): [item2, True, attachments]})
                await message.answer("команда добавлена с ответом")
            
            await file_editor.save_data(roleplay_command, "roleplay.json")

@roleplay_labeler.message()
async def send_roleplay(message: Message):
    config = file_editor.open_data("config.json")
    if config.get("delay") != 0:
        config.update({"delay_now": config.get("delay_now") + 1})

        if config.get("delay_now") > config.get("delay"):
            config.update({"delay_now": 0})
            posts = await vk_api.wall.get(owner_id=group_id, count=100)

            post = random.choice(posts.items)

            await message.answer(post.text, attachment = await get_attachments(post.attachments))
        
        await file_editor.save_data(config, "config.json")

    text = message.text.lower()

    if text in roleplay_command:
        user = await message.get_user(fields='domain')

        attachment = random.choice(roleplay_command.get(text)[2])

        if roleplay_command.get(text)[1] == False:
            await message.answer(f"[id{message.from_id}|{await get_user(message.peer_id, message.from_id, user.first_name + ' ' + user.last_name)}] {roleplay_command.get(text)[0]}",
                                  attachment=attachment)
        
        if roleplay_command.get(text)[1] == True and message.reply_message != None:
            user_reply = await message.reply_message.get_user()

            await message.answer(f"[id{message.from_id}|{await get_user(message.peer_id, message.from_id, user.first_name + ' ' + user.last_name)}]" +
                                 f" {roleplay_command.get(text)[0]} [id{message.reply_message.from_id}|{await get_user(message.reply_message.chat_id, message.reply_message.from_id, user_reply.first_name + ' ' + user_reply.last_name)}]", attachment=attachment)
        