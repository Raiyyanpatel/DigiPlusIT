import asyncio
import json
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings

async def main():
    llm = ChatGoogleGenerativeAI(
        api_key=settings.GEMINI_API_KEY, 
        model="gemini-flash-latest", 
        temperature=0
    ).bind(response_format={"type": "json_object"})
    
    res = await llm.ainvoke([HumanMessage(content="return json {'a':1}")])
    print(type(res.content))
    print(res.content)
    
    if isinstance(res.content, list):
        print("LIST FOUND")
        print(type(res.content[0]))
        if isinstance(res.content[0], dict) and 'text' in res.content[0]:
            print(res.content[0]['text'])

asyncio.run(main())
