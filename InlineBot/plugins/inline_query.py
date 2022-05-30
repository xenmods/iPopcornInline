

import re
import ast
from InlineBot import (
    CodeXBotz,
    Message,
    thumb,
    filters,
    InlineQuery,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultPhoto,
    InputTextMessageContent,
    InlineQueryResultArticle,
    InlineQueryResultCachedPhoto,
    InlineQueryResultCachedDocument
)
from InlineBot.database import (
    get_alerts,
    get_filters
)

@CodeXBotz.on_message(filters.private & filters.command('search'))
async def give_filter(client: CodeXBotz, query: Message):
    text = query.text.lower().replace('/search ', '')
    documents = await get_filters(text)
    results = []
    for document in documents:
        reply_text = document['reply']
        button = document['btn']
        alert = document['alert']
        fileid = document['file']
        keyword = document['text']
        msg_type = document['type']

        if button == "[]":
            button = None
        
        if reply_text:
            reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")
            
        if fileid == 'None':
            try:
                result = await query.reply_text(reply_text, disable_web_page_preview=True, reply_markup=None if button ==  None else InlineKeyboardMarkup(eval(button)), parse_mode = 'html')
#                 result = InlineQueryResultArticle(
#                     title=keyword.upper(),
#                     input_message_content=InputTextMessageContent(message_text = reply_text, disable_web_page_preview = True,
#                         parse_mode = 'html'),
#                     description='Text',
#                     thumb_url = thumb,
#                     reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
#                 )
            except:
                continue
        elif msg_type == 'Photo':
            try:
                result = await query.reply_photo(photo=fileid, caption=reply_text or '', reply_markup=None if button ==  None else InlineKeyboardMarkup(eval(button)), parse_mode = 'html')
#                 result = InlineQueryResultPhoto(
#                     photo_url = fileid,
#                     title = keyword.upper(),
#                     description = 'Photo',
#                     parse_mode = 'html',
#                     caption = reply_text or '',
#                     reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
#                 )
            except:
                continue
        elif fileid:
            try:
                result = await client.send_cached_media(chat_id=query.chat_id, file_id=fileid, caption=reply_text or '', parse_mode='html', reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button)))
#                 result = InlineQueryResultCachedDocument(
#                     title = keyword.upper(),
#                     file_id = fileid,
#                     caption = reply_text or "",
#                     parse_mode = 'html',
#                     description = msg_type,
#                     reply_markup= None if button ==  None else InlineKeyboardMarkup(eval(button))
#                 )
            except:
                continue
        else:
            return await query.reply_text('Not Found❗Please Type Correct Spelling.👇🏻')
    
#         results.append(result)
        
#     if len(results) != 0:
#         switch_pm_text = f"Show {len(results)} Search More.🔍"
#     else:
#         switch_pm_text = "Not Found❗Please Type Correct Spelling.👇🏻"

#     await query.answer(
#         results = results,
#         is_personal = True,
#         switch_pm_text = switch_pm_text,
#         switch_pm_parameter = 'start'
#     )
        
        
@CodeXBotz.on_callback_query(filters.regex(r"^(alertmessage):(\d):(.*)"))
async def alert_msg(client: CodeXBotz, callback: CallbackQuery):
    regex = r"^(alertmessage):(\d):(.*)"
    matches = re.match(regex, callback.data)
    i = matches.group(2)
    id = matches.group(3)
    alerts = await get_alerts(id)
    
    if alerts:
        alerts = ast.literal_eval(alerts)
        alert = alerts[int(i)]
        alert = alert.replace("\\n", "\n").replace("\\t", "\t")
        try:
            await callback.answer(alert,show_alert=True)
        except:
            pass
