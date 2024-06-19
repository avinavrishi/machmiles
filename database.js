const sqlite3 = require('sqlite3').verbose();

// Connect to the SQLite database
const db = new sqlite3.Database('flightbooking.db', (err) => {
    if (err) {
        console.error('Error connecting to the database:', err.message);
    } else {
        console.log('Connected to the SQLite database.');
        createTables(); // Call function to create tables after connecting
    }
});

// Function to create tables if they don't exist
function createTables() {
    // SQL commands to create tables
    const createUsersTable = `
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    `;

    const createBookingsTable = `
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            flight_number TEXT NOT NULL,
            departure_date TEXT NOT NULL,
            arrival_date TEXT NOT NULL,
            departure_airport TEXT NOT NULL,
            arrival_airport TEXT NOT NULL,
            seat_class TEXT NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    `;

    const createPaymentsTable = `
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            card_number TEXT NOT NULL,
            card_holder_name TEXT NOT NULL,
            expiration_date TEXT NOT NULL,
            cvv TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    `;

    // Execute SQL commands to create tables
    db.serialize(() => {
        db.run(createUsersTable, (err) => {
            if (err) {
                console.error('Error creating users table:', err.message);
            } else {
                console.log('Users table created successfully.');
            }
        });
        db.run(createBookingsTable, (err) => {
            if (err) {
                console.error('Error creating bookings table:', err.message);
            } else {
                console.log('Bookings table created successfully.');
            }
        });
        db.run(createPaymentsTable, (err) => {
            if (err) {
                console.error('Error creating payments table:', err.message);
            } else {
                console.log('Payments table created successfully.');
            }
        });
    });
}

// Export the database connection for use in other files
module.exports = db;
