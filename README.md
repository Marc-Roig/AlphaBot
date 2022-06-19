# ⚛️ AlphaBot - Railway version

Alphabot is a telegram bot that allows you to book Crossfit classes before the bookable time allowed in the official app.

![](./assets/alphabot.png)

## 🚀 Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/1lUfdC?referralCode=77g3LA)

Fill the following env vars as per below instructions: 

> BOX_ID = 9287  ⚠ Don't touch this
>
> MONGO_CONNECTION = ... 
> 
> MONGO_DB = ...
> 

# TODO

- Tidy commands
    - Create callback query handler folder
    - Create mess handler folder
    - Create command handler folder

- Create public command to ask for an invite
- [TO TEST] Create user command to list your bookings
- Create user command to ask for booking validation
- Test app for a week
- [TO TEST] Move to redis / mongo / postgres
- Message user ok booking scheduled booking
- Retries for booking
- [TO TEST] If you do not have more bookings available discard booking
- Add logger (loguru)