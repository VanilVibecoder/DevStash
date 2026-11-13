import httpx

from aiogram import Router, F
from aiogram.types import Message
import openai
from article_parser import parse_page
from agent import summarize_text



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
                    await message.answer("Generating answer...")
                    try:
                        summary_of_text = await summarize_text(parsed_text)
                        await message.answer(summary_of_text, parse_mode="HTML")
                    
                    # except API error
                    except ValueError:
                        await message.answer("LLM no return text. Please try again later.")
                    except openai.APITimeoutError:
                        await message.answer("LLM response timed out. Please try again later.", parse_mode="HTML")
                    
                    # except connection error
                    except openai.APIConnectionError:
                        await message.answer("Error of connection to the language model. Please try again later.", parse_mode="HTML")
                    
                    # except API status error
                    except openai.APIStatusError:
                        error = openai.APIStatusError.status_code
                        if error == 401:
                            await message.answer(f"Error {error}. Problem of authorization.", parse_mode="HTML")
                        elif error == 429:
                            await message.answer(f"Error {error}. Request limit: trying again later might help ", parse_mode="HTML")
                        elif error == 500:
                            await message.answer(f"Error {error}. Server issue: trying again later might help", parse_mode="HTML")
                        else:
                            await message.answer(f"Error {error}.", parse_mode="HTML")


        except httpx.TimeoutException:
            await message.answer("The link took too long to open. Please try again later.", parse_mode="HTML")
        
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            if status == 404:
                await message.answer(f"Page not found (error {status})", parse_mode="HTML")
            elif status == 403:
                await message.answer(f"Access denied (error {status})", parse_mode="HTML")
            else:
                await message.answer(f"HTTP error (error {status})", parse_mode="HTML")
            
            
        except httpx.RequestError as e:
            await message.answer(f"Error opening the link: {e}", parse_mode="HTML")
        
        
        