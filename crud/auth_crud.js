const db = require('../database');

// CRUD operations for the users table
// Create a new user
function createUser(username, password, email, is_admin, callback) {
    const sql = `INSERT INTO users (username, password, email, is_admin) VALUES (?, ?, ?, ?)`;
    db.run(sql, [username, password, email, is_admin], function(err) {
        callback(err, this ? this.lastID : null);
    });
}

// Get a user by ID
function getUser(username, callback) {
    const sql = `SELECT * FROM users WHERE username = ?`;
    db.get(sql, [username], (err, row) => {
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

// Get all users
function getAllUsers(callback) {
    const sql = `SELECT * FROM users`;
    db.all(sql, [], (err, rows) => {
        callback(err, rows);
    });
}

module.exports = {
    createUser,
    getUser,
    updateUser,
    deleteUser,
    getAllUsers,
}