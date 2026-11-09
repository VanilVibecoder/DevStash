import httpx

from aiogram import Router, F
from aiogram.types import Message


links_router = Router()

@links_router.message(F.text.startswith("http://") | F.text.startswith("https://"))
async def handle_link(message: Message):
    url = message.text.strip()
    await message.answer("Checking the link, please wait...")
    
    
    # open the link and check its
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            if response.status_code == 200:
                await message.answer(f"Link succesfully opened!")
                await message.answer(response.text)
        
        except httpx.TimeoutException:
            await message.answer("The link took too long to open. Please try again later.")
        
        except httpx.HTTPStatusError as e:
            await message.answer(f"Error opening the link: {e}")
        
        except httpx.RequestError as e:
            await message.answer(f"Error opening the link: {e}")
            