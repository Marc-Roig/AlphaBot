# ⚛️ AlphaBot - Railway version
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/1lUfdC?referralCode=77g3LA)

Alphabot is a telegram bot that allows you to book Crossfit classes before the bookable time allowed in the official app.

![](./assets/alphabot.png)


# 📦 Database migrations

Used when a release introduces new fields into the database or breaking changes.
```
pymongo-migrate migrate -u 'mongodb://mongo:PASSWORD@containers-us-west-74.railway.app:6234/test?authSource=admin' -m migrations
````


# ✨ Features

- Book / Cancel a class.
- Schedule a booking when is more than 4 days ahead.
- Schedule a booking when class is full.
- Aimharder login
- Notifications
    - Scheduled booking succeeded
    - Scheduled booking failed


# 💁‍♀️ How to use

```
pip install -r requirements.txt
python alphabot.py
```

# 🛣️ Roadmap

## 🔖 Release 0.2.0
- [X] If you do not have more bookings available discard booking (🧪 Test pending)
- [X] Add timestamps to database entities (createdAt and updatedAt)
- [X] Database migrations (🧪 Test pending)
- [X] Message user an scheduled booking has succeeded (🧪 Test pending)
- [X] Message user an scheduled booking has failed (🧪 Test pending)
- [X] Create public command to ask for an invite (🧪 Test pending)


## 🔖 Release 0.3.0
- [ ] Show class members
- [ ] Do not go backwards in calendar
- [ ] Remove past days and use a - 
- [ ] Remove todays classes that already have started
- [ ] Log in reminder every 2 months
- [ ] Add logger (loguru) ~
- [ ] Create domain entities for 
    - [ ] User
    - [ ] Scheduled Booking
    - [ ] Telegram User
    
## 🔖 Release 0.4.0
- [ ] Reminder of today and 4 days scheduling bookings every morning (4 days) with a button to disable this message
- [ ] Create user command to ask for booking validation
- [ ] Tidy commands
    - Create callback query handler folder
    - Create mess handler folder
    - Create command handler folder



