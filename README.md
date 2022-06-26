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

# 🛣️ Road map

## 🔖 Future releases
- [ ] Add logger (loguru) ~
- [ ] Reminder of today and 4 days scheduling bookings every morning (4 days) with a button to disable this message

# 🧪 Testing steps
[ ] Book a class
[ ] Cancel a class
[ ] Schedule a booking when is more than 4 days ahead
[ ] Schedule a booking when class is full
[ ] Discard a booking when 
    [ ] Exceeded Daily Booking Limit
    [ ] Not Allowed For that Class
    [ ] Exceeded Booking Limit
    [ ] Can not Book at the same time
[ ] Aimharder login
[ ] Notifications
    [ ] Scheduled booking succeeded
    [ ] Scheduled booking failed
    [ ] Login about to expire
[ ] Database migrations
[ ] Invite
