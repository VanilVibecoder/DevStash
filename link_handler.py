import httpx

from aiogram import Router, F
from aiogram.types import Message
from article_parser import parse_page

links_router = Router()


headers = {
    "user-agent": "IvanProgerFireFox"
}
@links_router.message(F.text.startswith("http://") | F.text.startswith("https://"))
async def handle_link(message: Message):
    url = message.text.strip()
    await message.answer("Checking the link, please wait...")
    
    
    # open the link and check its
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=5.0)
            # check if the link is opened successfully
            response.raise_for_status()
            if response.status_code == 200:
                await message.answer(f"Link succesfully opened!")
                text = response.text
                parsed_text = parse_page(text)
                # parse the page content and send it to the user
                if parsed_text is None:
                    await message.answer("The link does not contain any text.")
                else:
                    await message.answer(parsed_text[0:500])

        except httpx.TimeoutException:
            await message.answer("The link took too long to open. Please try again later.")
        
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status == 404:
                await message.answer(f"Page not found (error {status})")
            elif status == 403:
                await message.answer(f"Access denied (error {status})")
            else:
                await message.answer(f"HTTP error (error {status})")
            
            
        except httpx.RequestError as e:
            await message.answer(f"Error opening the link: {e}")
            