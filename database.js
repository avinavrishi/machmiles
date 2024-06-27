const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');

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
            email TEXT NOT NULL UNIQUE,
            is_admin INTEGER,
            is_staff INTEGER
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

    const createPostsTable = `
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author TEXT NOT NULL,
            date_created TEXT NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    `;

    const createCategoriesTable = `
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    `;

    const createCommentsTable = `
        CREATE TABLE IF NOT EXISTS comments (
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            date_created TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(post_id)
        )
    `;

    // Execute SQL commands to create tables
    db.serialize(() => {
        db.run(createUsersTable, (err) => {
            if (err) {
                console.error('Error creating users table:', err.message);
            } else {
                console.log('Users table checked/created successfully.');
            }
        });
        db.run(createBookingsTable, (err) => {
            if (err) {
                console.error('Error creating bookings table:', err.message);
            } else {
                console.log('Bookings table checked/created successfully.');
            }
        });
        db.run(createPaymentsTable, (err) => {
            if (err) {
                console.error('Error creating payments table:', err.message);
            } else {
                console.log('Payments table checked/created successfully.');
            }
        });
        db.run(createCategoriesTable, (err) => {
            if (err) {
                console.error('Error creating categories table:', err.message);
            } else {
                console.log('Categories table checked/created successfully.');
            }
        });
        db.run(createPostsTable, (err) => {
            if (err) {
                console.error('Error creating posts table:', err.message);
            } else {
                console.log('Posts table checked/created successfully.');
            }
        });
        db.run(createCommentsTable, (err) => {
            if (err) {
                console.error('Error creating comments table:', err.message);
            } else {
                console.log('Comments table checked/created successfully.');
            }

            // After all tables are created, check/create admin user
            checkCreateAdmin();
        });
    });
}

function checkCreateAdmin() {
    const adminUsername = 'admin';
    const adminEmail = 'admin@gmail.com';
    const adminPassword = 'Admin@123';
    const isAdmin = 1;

    // Check if admin user already exists
    const checkAdminQuery = `SELECT * FROM users WHERE username = ?`;
    db.get(checkAdminQuery, [adminUsername], async (err, row) => {
        if (err) {
            console.error('Error checking admin user:', err.message);
            return;
        }

        // If admin user does not exist, create one
        if (!row) {
            try {
                const hashedPassword = await bcrypt.hash(adminPassword, 10);
                const insertAdminQuery = `INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)`;
                db.run(insertAdminQuery, [adminUsername, hashedPassword, adminEmail, isAdmin], (err) => {
                    if (err) {
                        console.error('Error creating admin user:', err.message);
                    } else {
                        console.log('Admin user created successfully.');
                    }
                });
            } catch (error) {
                console.error('Error hashing admin password:', error.message);
            }
        } else {
            console.log('Admin user already exists.');
        }
    });
}

// Export the database connection for use in other files
module.exports = db;
