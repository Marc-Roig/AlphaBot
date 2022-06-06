Telegram automated bot to :
- List available clases for a day.
- Book a class in range.
- Book a class that is full.
- Book a class that is not in range.



- Use python
- Hardcode the cookie token 


# Presentation:

## Telegram bot

- List my bookings (with user Id)
- Make booking ( with user Id and booking ID)

## Endpoints

## Cron

- Every minute check if there are any bookings to make per user
- Make booking if the penidng bookings have dates greater than current.



# Infrastructure:

enum Classes {

}

Booking
    getBooking(date: Date, name: string)
    book(booking: Booking) -> Booking
        - Makes a request to book.
        - If it does not work throw error.
        - Changes status of booking
    scheduleBooking(booking: Booking)
        - Stores in a dictionary
    cancelBooking
User
    getCookie(userName)

