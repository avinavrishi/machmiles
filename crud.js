const db = require('./database');

// CRUD operations for the users table

// Create a new user
function createUser(username, password, email, callback) {
    const sql = `INSERT INTO users (username, password, email) VALUES (?, ?, ?)`;
    db.run(sql, [username, password, email], function(err) {
        callback(err, this ? this.lastID : null);
    });
}

// Get a user by ID
function getUser(userId, callback) {
    const sql = `SELECT * FROM users WHERE user_id = ?`;
    db.get(sql, [userId], (err, row) => {
        callback(err, row);
    });
}

// Update a user by ID
function updateUser(userId, username, password, email, callback) {
    const sql = `UPDATE users SET username = ?, password = ?, email = ? WHERE user_id = ?`;
    db.run(sql, [username, password, email, userId], function(err) {
        callback(err, this ? this.changes : null);
    });
}

// Delete a user by ID
function deleteUser(userId, callback) {
    const sql = `DELETE FROM users WHERE user_id = ?`;
    db.run(sql, [userId], function(err) {
        callback(err, this ? this.changes : null);
    });
}

// CRUD operations for the bookings table

// Create a new booking
function createBooking(userId, flightNumber, departureDate, arrivalDate, departureAirport, arrivalAirport, seatClass, price, callback) {
    const sql = `INSERT INTO bookings (user_id, flight_number, departure_date, arrival_date, departure_airport, arrival_airport, seat_class, price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)`;
    db.run(sql, [userId, flightNumber, departureDate, arrivalDate, departureAirport, arrivalAirport, seatClass, price], function(err) {
        callback(err, this ? this.lastID : null);
    });
}

// Get a booking by ID
function getBooking(bookingId, callback) {
    const sql = `SELECT * FROM bookings WHERE booking_id = ?`;
    db.get(sql, [bookingId], (err, row) => {
        callback(err, row);
    });
}

// Update a booking by ID
function updateBooking(bookingId, flightNumber, departureDate, arrivalDate, departureAirport, arrivalAirport, seatClass, price, callback) {
    const sql = `UPDATE bookings SET flight_number = ?, departure_date = ?, arrival_date = ?, departure_airport = ?, arrival_airport = ?, seat_class = ?, price = ? WHERE booking_id = ?`;
    db.run(sql, [flightNumber, departureDate, arrivalDate, departureAirport, arrivalAirport, seatClass, price, bookingId], function(err) {
        callback(err, this ? this.changes : null);
    });
}

// Delete a booking by ID
function deleteBooking(bookingId, callback) {
    const sql = `DELETE FROM bookings WHERE booking_id = ?`;
    db.run(sql, [bookingId], function(err) {
        callback(err, this ? this.changes : null);
    });
}

// CRUD operations for the payments table

// Create a new payment
function createPayment(userId, cardNumber, cardHolderName, expirationDate, cvv, callback) {
    const sql = `INSERT INTO payments (user_id, card_number, card_holder_name, expiration_date, cvv) VALUES (?, ?, ?, ?, ?)`;
    db.run(sql, [userId, cardNumber, cardHolderName, expirationDate, cvv], function(err) {
        callback(err, this ? this.lastID : null);
    });
}

// Get a payment by ID
function getPayment(paymentId, callback) {
    const sql = `SELECT * FROM payments WHERE payment_id = ?`;
    db.get(sql, [paymentId], (err, row) => {
        callback(err, row);
    });
}

// Update a payment by ID
function updatePayment(paymentId, cardNumber, cardHolderName, expirationDate, cvv, callback) {
    const sql = `UPDATE payments SET card_number = ?, card_holder_name = ?, expiration_date = ?, cvv = ? WHERE payment_id = ?`;
    db.run(sql, [cardNumber, cardHolderName, expirationDate, cvv, paymentId], function(err) {
        callback(err, this ? this.changes : null);
    });
}

// Delete a payment by ID
function deletePayment(paymentId, callback) {
    const sql = `DELETE FROM payments WHERE payment_id = ?`;
    db.run(sql, [paymentId], function(err) {
        callback(err, this ? this.changes : null);
    });
}

module.exports = {
    createUser,
    getUser,
    updateUser,
    deleteUser,
    createBooking,
    getBooking,
    updateBooking,
    deleteBooking,
    createPayment,
    getPayment,
    updatePayment,
    deletePayment
};
