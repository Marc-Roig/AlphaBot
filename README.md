# ⚛️ AlphaBot - Railway version

Alphabot is a telegram bot that allows you to book Crossfit classes before the bookable time allowed in the official app.

![](./assets/alphabot.png)

# 🚀 Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/1lUfdC?referralCode=77g3LA)

Make sure to use the env vars defined in app.json.

# 📦 Database migrations

Used when a release introduces new fields into the database or breaking changes.
```
pymongo-migrate migrate -u 'mongodb://mongo:PASSWORD@containers-us-west-74.railway.app:6234/test?authSource=admin' -m migrations
````

# ✨ Features

# 💁‍♀️ How to use

# 📝 TODO


- [X] If you do not have more bookings available discard booking (🧪 Test pending)
- [X] Test app for a week (🧪 Test pending)
- [ ] Add timestamps to database entities (createdAt and updatedAt)
    - [ ] Test beanie migrations
- [ ] Message user ok booking scheduled booking
- [ ] Message user if class is canceled 
- [ ] Create public command to ask for an invite
- [ ] Create user command to ask for booking validation
- [ ] Retries for booking
- [ ] Add logger (loguru) ~
- [ ] Tidy commands
    - Create callback query handler folder
    - Create mess handler folder
    - Create command handler folder
- [ ] Other users scheduled not working
- [ ] Show class members
- [ ] Do not go backwards in calendar
- [ ] Remove past days and use a - 
- [ ] Reminder of today and 4 days scheduling bookings every morning (4 days) with a button to disable this message
- [ ] Log in reminder every 2 months