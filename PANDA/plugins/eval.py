# Copyright (c) 2026 khithlainhtet
# Licensed under the MIT License.
# This file is part of PANDA

import io
import os
import re
import sys
import uuid
import traceback
from html import escape
from typing import Any, Optional, Tuple

from pyrogram import filters, types

from PANDA import anon, app, config, db, lang, userbot
from PANDA.helpers import format_exception, meval


@app.on_message(filters.command(["eval", "exec"]) & filters.user([config.OWNER_ID, config.ERROR_FORMAT]))
@app.on_edited_message(filters.command(["eval", "exec"]) & filters.user([config.OWNER_ID, config.ERROR_FORMAT]))
@lang.language()
async def eval_handler(_, message: types.Message):
    if len(message.command) < 2:
        
        return await message.reply_text("ပေးထားတဲ့ code ကို run ဖို့ input လိုအပ်ပါတယ်ဗျာ။")

    code = message.text.split(None, 1)[1]
    out_buf = io.StringIO()

    async def _eval_code() -> Tuple[str, Optional[str]]:
        async def send(*args: Any, **kwargs: Any) -> types.Message:
            return await message.reply_text(*args, **kwargs)

        def _print(*args: Any, **kwargs: Any) -> None:
            kwargs.setdefault("file", out_buf)
            print(*args, **kwargs)

        eval_vars = {
            "m": message,
            "r": message.reply_to_message,
            "chat": message.chat,
            "user": message.from_user,
            "app": app,
            "anon": anon,
            "db": db,
            "client": app,
            "ub": userbot,
            "ikb": types.InlineKeyboardButton,
            "ikm": types.InlineKeyboardMarkup,
            "send": send,
            "config": config,
            "print": _print,
            "os": os,
            "re": re,
            "sys": sys,
            "tb": traceback,
        }

        try:
            
            result = await meval(code, globals(), **eval_vars)
            return "", result
        except Exception as e:
            
            tb = traceback.extract_tb(e.__traceback__)
            snippet_tb = next(
                (i for i, f in enumerate(tb) if f.filename == "<string>"), -1
            )
            formatted_tb = format_exception(
                e, tb[snippet_tb:] if snippet_tb != -1 else tb
            )
            return "Error အကျဉ်းချုပ်:", formatted_tb

    _, result = await _eval_code()

    if result is not None or not out_buf.getvalue():
        print(result, file=out_buf)

    output = out_buf.getvalue().strip()
    
    
    if len(output) > 4000:
        with io.BytesIO(output.encode()) as out_file:
            out_file.name = f"eval_{uuid.uuid4().hex[:5]}.txt"
            return await message.reply_document(
                document=out_file, 
                caption="Output အရမ်းရှည်လို့ File အနေနဲ့ ပို့ပေးလိုက်ပါတယ်ဗျာ။",
                disable_notification=True
            )

    
    await message.reply_text(f"**Output:**\n`{escape(output)}`" if output else "**Output:** `None`")
