import asyncio
import httpx
from abc import ABC, abstractmethod
from tenacity import retry, AsyncRetrying, stop_after_attempt

from re import Pattern
from telegram import Update
from telegram.ext import ContextTypes

from utils.create_page import create_page

class Preview(ABC):
    def __init__(self, pattern:Pattern, channel:str = '', channel_url:str = '', headers = {}, show_origin = False) -> None:
        self.pattern = pattern
        self.channel = channel
        self.channel_url = channel_url
        self.headers = headers
        self.show_origin = show_origin
    
    async def clean_url(self, URL:str) -> str:
        return URL
    
    @retry(stop = stop_after_attempt(5))
    async def get_res(self, URL:str):
        URL = await self.clean_url(URL)
        async with httpx.AsyncClient() as client:
            res = await client.get(URL, headers = self.headers)
        return res
    
    @abstractmethod
    def viewer(self, res):
        pass # soup to (title, author, content)
    
    async def to_telegraph(self, URL:str) -> str:
        # (title, author, content) to a list of telegraph URL.
        soup = await self.get_res(URL)
        title, author, content = self.viewer(soup)
        res = await create_page(title, content, author = author, author_url=self.channel_url)
        if len(res) == 1:
            responses = [f'[{title}]({url})' for url in res]
        else:
            responses = [f'[{title}({i+1})]({url})' for i, url in enumerate(res)]
        if self.show_origin:
            responses = [r + f' | [原文]({URL})' for r in responses]
        return responses
    
    async def preview(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        URL = context.match.group(0)
        responses = await self.to_telegraph(URL)
        for r in responses:
            async for attempt in AsyncRetrying(stop=stop_after_attempt(5)):
                with attempt:
                    await update.message.reply_text(r, parse_mode = "Markdown")