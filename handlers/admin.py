from vkbottle.bot import BotLabeler, Message, rules
from vkbottle import API
from typing import Optional
from file import file_editor

admin_labeler = BotLabeler()
admin_labeler.vbml_ignore_case = True
file_edit = file_editor
    
config = file_editor.open_data("config.json")

@admin_labeler.message(text="бот админ")
async def send_callback_button(message: Message, item: Optional[str] = None):
    if message.from_id in config.get("admins") and message.reply_message:
        if message.reply_message.from_id not in config.get("admins"):
            config.get("admins").append(message.reply_message.from_id)
            
            await message.answer("Админ назначен")
            await file_editor.save_data(config, "config.json")

@admin_labeler.message(text=["репост <item> смс", "репост смс"])
async def send_callback_button(message: Message, item: Optional[str] = None):
    global delay
    if message.from_id in config.get("admins"):
        if item is None:
            await message.answer("репост <например 500> смс")
        else:   
            config.update({"delay": int(item)})
            delay = int(item)
            
            await message.answer("Выполнено")
            await file_editor.save_data(config, "config.json")

        
