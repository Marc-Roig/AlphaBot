"""
Release 0.0.2

These release adds some breaking changes into the database:
- Adding timestamps to every entity (created_at, updated_at).
- Added retries field in scheduled bookings.

"""
import pymongo
import datetime

name = '20220620113231'
dependencies: list = []


def upgrade(db: pymongo.database.Database) -> None:

    users_coll = db['Users']
    telegram_users_coll = db['TelegramUsers']
    scheduled_bookings_coll = db['ScheduledBookings']
    
    users_coll.update_many({}, {"$set": {
        "updated_at": datetime.datetime.now(),
        "created_at": datetime.datetime.now(),
    }})
    
    telegram_users_coll.update_many({}, {"$set": {
        "updated_at": datetime.datetime.now(),
        "created_at": datetime.datetime.now(),
    }})

    scheduled_bookings_coll.update_many({}, {"$set": {
        "updated_at": datetime.datetime.now(),
        "created_at": datetime.datetime.now(),
        "retries": 0
    }})

def downgrade(db: pymongo.database.Database) -> None:
    
    users_coll = db['Users']
    telegram_users_coll = db['TelegramUsers']
    scheduled_bookings_coll = db['ScheduledBookings']

    users_coll.update_many({}, {"$unset": {
        "updated_at": "",
        "created_at": "",
    }})

    telegram_users_coll.update_many({}, {"$unset": {
        "updated_at": "",
        "created_at": "",
    }})

    scheduled_bookings_coll.update_many({}, {"$unset": {
        "updated_at": "",
        "created_at": "",
        "retries": 0
    }})