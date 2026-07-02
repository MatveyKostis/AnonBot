from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import settings
from bot.utils.captcha import generate_captcha
from bot.utils.db import db
from bot.utils.i18n import _

router = Router()

class CaptchaStates(StatesGroup):
    waiting_for_captcha = State()

@router.message(CommandStart())
async def cmd_start(message: Message, locale: str):
    db.log_user(message.from_user)
    await message.answer(_("welcome", locale=locale))

@router.message(CaptchaStates.waiting_for_captcha)
async def process_captcha(message: Message, state: FSMContext, bot: Bot, locale: str):
    data = await state.get_data()
    correct_captcha = data.get("captcha_text")
    original_msg_id = data.get("original_msg_id")
    
    if message.text and message.text.upper() == correct_captcha:
        await state.clear()
        
        try:
            db_msg_id = data.get("db_msg_id", "N/A")
            prefix = f"Forwarding, ID [{db_msg_id}]:"
            target_chat_id = settings.group_chat_id
            
            if data.get('has_media'):
                new_caption = prefix
                if data.get('original_caption'):
                    new_caption += f"\n{data.get('original_caption')}"
                
                await bot.copy_message(
                    chat_id=target_chat_id,
                    from_chat_id=message.chat.id,
                    message_id=original_msg_id,
                    caption=new_caption
                )
            elif data.get('is_text'):
                await bot.send_message(
                    chat_id=target_chat_id,
                    text=f"{prefix}\n{data.get('original_text')}"
                )
            else:
                # Other types (stickers, etc.)
                await bot.copy_message(
                    chat_id=target_chat_id,
                    from_chat_id=message.chat.id,
                    message_id=original_msg_id
                )
                await bot.send_message(chat_id=target_chat_id, text=prefix)
            
            await message.answer(_("captcha_solved", locale=locale))
            
        except Exception as e:
            await message.answer(_("captcha_error", locale=locale))
            print(f"Error forwarding: {e}")
    else:
        # Generate new captcha
        captcha_text, captcha_img = generate_captcha()
        await state.update_data(captcha_text=captcha_text)
        await message.answer_photo(
            BufferedInputFile(captcha_img, filename="captcha.png"),
            caption=_("incorrect_captcha", locale=locale)
        )

@router.message(F.chat.type == "private")
async def handle_any_message(message: Message, state: FSMContext, locale: str):
    # Log everything
    db_msg_id = db.log_message(message)
    
    # Generate captcha
    captcha_text, captcha_img = generate_captcha()
    
    has_media = bool(message.photo or message.video or message.document or message.audio or message.voice)
    is_text = bool(message.text)
    
    await state.set_state(CaptchaStates.waiting_for_captcha)
    await state.update_data(
        captcha_text=captcha_text,
        db_msg_id=db_msg_id,
        original_msg_id=message.message_id,
        original_text=message.text,
        original_caption=message.caption,
        has_media=has_media,
        is_text=is_text
    )
    
    await message.answer_photo(
        BufferedInputFile(captcha_img, filename="captcha.png"),
        caption=_("solve_captcha", locale=locale)
    )
