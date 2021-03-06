import base64
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment, Message
from nonebot.typing import T_State
from nonebot.params import State, CommandArg

from .data_source import *

__usage__ = """
/字符画 <图片>
""".strip()

pic2text = on_command("字符画", priority=26, block=True)


@pic2text.handle()
async def _(args: Message = CommandArg(), state: T_State = State()):
    for seg in args:
        if seg.type == 'image':
            state['image'] = Message(seg)


@pic2text.got('image', prompt='图呢？')
async def generate_(bot: Bot, event: Event, state: T_State = State()):
    msg = state['image']
    if msg[0].type == "image":
        url = msg[0].data["url"]  # 图片链接
        await pic2text.send("努力生成中...")
        
        pic = await get_img(url)  # 取图
        if not pic:
            await pic2text.finish(event, message="图片未获取到，请稍后再试")

        if pic.format == 'GIF':
            res = await char_gif(pic) 
            await pic2text.finish(
                MessageSegment.image(
                       f"base64://{base64.b64encode(res.getvalue()).decode()}"
                   )
            )
        text = await get_pic_text(pic)
        if text:
            res = await text2img(text)  
            await pic2text.finish(
                MessageSegment.image(
                       f"base64://{base64.b64encode(res.getvalue()).decode()}"
                   )
            )
    else:
        await pic2text.finish('要的是图')
