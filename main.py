from fastapi import FastAPI
from alphabot import bot
import asyncio

app = FastAPI()


future = None
@app.get("/")
def read_root():
    return {"Hello": "World"}

	
@app.on_event("startup")
async def startup_event():
	loop = asyncio.get_event_loop()
	future = loop.run_in_executor(None, bot.polling)

@app.on_event("shutdown")
async def shutdown_event():
	bot.stop_bot()
	if future:
		future.cancel()