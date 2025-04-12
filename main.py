from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import random
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
voice_content = os.listdir(current_dir + "\\" + "voice_jp")   # 当前脚本所在目录

@register("astrbot_plugin_wsde", "bushikq", "维什戴尔随机语音插件", "2.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("wsde")
    async def wsde_handler(self, event: AstrMessageEvent, message: str=None,language:str='0'):
        """/wsde (语音名字) (jp/cn 默认日文)    随机维什戴尔游戏内语音。"""
        if language == "cn" or language == "1":
             language = "voice_cn"
        elif language != "jp" and language != "0":
             yield event.plain_result("死魂灵又在废话")
             return
        else:
             language = "voice_jp"
        voice_path =current_dir + "\\" + language  # 拼接voice子目录
        voice_content = os.listdir(voice_path)  # 获取voice子目录下所有文件
        if not message or message.strip() == "":
            voice_num = random.randint(0, len(voice_content)-1)
            voice_name = voice_content[voice_num]
        else:
            if message[-4::]!= ".wav":
                 voice_name = message + ".wav"
            else:
                 voice_name = message
        voice_adress = os.path.join(voice_path, voice_name)
        yield event.plain_result(f"{'__'+voice_name[:-4:]}")
        async for message in self.send_voice_message(event, voice_adress):
                        yield message # 发送语音消息
    @filter.command("wsde_list")
    async def wsde_list_handler(self, event: AstrMessageEvent):
        """/wsde_list    显示维什戴尔语音列表。"""
        yield event.plain_result("维什戴尔语音列表："+str(voice_content))
                        

    async def send_voice_message(self, event: AstrMessageEvent, voice_file_path: str):
        # 检查文件是否存在
        if not os.path.exists(voice_file_path):
            yield event.plain_result("语音文件不存在，请检查文件路径。")
            return
        chain = [Record.fromFileSystem(voice_file_path)]
        yield event.chain_result(chain)
