from astrbot.api.all import *
from astrbot.api.event import filter, AstrMessageEvent
import random
import os
from typing import List, Optional

@register("astrbot_plugin_wsde", "bushikq", "维什戴尔随机语音插件", "2.2")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.plugin_dir = os.path.abspath(os.path.dirname(__file__))
        self.voice_jp_dir = os.path.join(self.plugin_dir, "voice_jp")
        self.voice_cn_dir = os.path.join(self.plugin_dir, "voice_cn")

    def _get_voice_files(self, language: str) -> List[str]:
        """获取指定语言的语音文件列表"""
        voice_dir = self.voice_cn_dir if language == "voice_cn" else self.voice_jp_dir
        try:
            return [f for f in os.listdir(voice_dir) if f.endswith('.wav')]
        except OSError:
            return []

    def _get_voice_path(self, voice_name: str, language: str) -> Optional[str]:
        """获取语音文件的完整路径"""
        voice_dir = self.voice_cn_dir if language == "voice_cn" else self.voice_jp_dir
        voice_path = os.path.join(voice_dir, voice_name)
        return voice_path if os.path.exists(voice_path) else None

    @filter.command("wsde")
    async def wsde_handler(self, event: AstrMessageEvent, message: str = None, language: str = 'jp'):
        """/wsde (语音名字) (jp/cn 默认日文) 随机维什戴尔游戏内语音。"""
        try:
            # 处理语言参数
            if language.lower() in ["cn", "1"]:
                lang_dir = "voice_cn"
            elif language.lower() in ["jp", "0"]:
                lang_dir = "voice_jp"
            else:
                yield event.plain_result("死魂灵又在废话了")
                return

            # 获取语音文件列表
            voice_files = self._get_voice_files(lang_dir)
            if not voice_files:
                yield event.plain_result(f"未找到{language}语音文件")
                return

            # 处理语音文件名
            if not message:
                voice_name = random.choice(voice_files)
            else:
                voice_name = f"{message}.wav" if not message.endswith('.wav') else message
                if voice_name not in voice_files:
                    yield event.plain_result(f"未找到语音：{voice_name}")
                    return

            # 获取并播放语音
            voice_path = self._get_voice_path(voice_name, lang_dir)
            if not voice_path:
                yield event.plain_result("语音文件不存在")
                return

            yield event.plain_result(f"正在播放：{voice_name[:-4]}")
            async for msg in self.send_voice_message(event, voice_path):
                yield msg

        except Exception as e:
            yield event.plain_result(f"播放语音时出错：{str(e)}")

    @filter.command("wsde_list")
    async def wsde_list_handler(self, event: AstrMessageEvent, language: str = 'jp'):
        """/wsde_list (jp/cn) 显示维什戴尔语音列表。"""
        try:
            lang_dir = "voice_cn" if language.lower() == "cn" else "voice_jp"
            voice_files = self._get_voice_files(lang_dir)
            
            if not voice_files:
                yield event.plain_result(f"未找到{language}语音文件")
                return

            voice_names = [name[:-4] for name in sorted(voice_files)]
            yield event.plain_result(f"维什戴尔{language}语音列表：\n" + "\n".join(voice_names))

        except Exception as e:
            yield event.plain_result(f"获取语音列表时出错：{str(e)}")

    async def send_voice_message(self, event: AstrMessageEvent, voice_file_path: str):
        """发送语音消息"""
        try:
            chain = [Record.fromFileSystem(voice_file_path)]
            yield event.chain_result(chain)
        except Exception as e:
            yield event.plain_result(f"发送语音消息时出错：{str(e)}")