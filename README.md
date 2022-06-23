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

## 🔖 Release 0.2.0
- [X] If you do not have more bookings available discard booking (🧪 Test pending)
- [X] Add timestamps to database entities (createdAt and updatedAt)
- [X] Database migrations (🧪 Test pending)
- [X] Message user an scheduled booking has succeeded (🧪 Test pending)
- [X] Message user an scheduled booking has failed (🧪 Test pending)
- [X] Create public command to ask for an invite (🧪 Test pending)
- [X] Show number of class members
- [X] Remove cancellation or booking message from user
- [X] Do not go backwards in calendar
- [X] Remove past days and use a - 
- [X] Button to close class selection from a given day. 
- [X] Log in reminder every 2 months
- [X] Remove todays classes that already have started
- [X] Send message to all users

## 🔖 Release 0.3.0
- [ ] Add how to m enu with gifs to show how to do everything
- [ ] Unify all handlers names in telegram commands
- [ ] Show more buttons in help message if you are an admin
- [ ] Remove Select class from X X message.
- [ ] Add logger (loguru) ~
- [ ] Add release notes message to telegram users
- [ ] Add how it works notes for new users
- [ ] Reminder of today and 4 days scheduling bookings every morning (4 days) with a button to disable this message
- [ ] Create user command to ask for booking validation


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
