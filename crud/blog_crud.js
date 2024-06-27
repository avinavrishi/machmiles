const db = require('../database');

// CRUD operations for Categories
const categoryCRUD = {
    create: (name, description, callback) => {
        const sql = 'INSERT INTO categories (name, description) VALUES (?, ?)';
        db.run(sql, [name, description], function(err) {
            callback(err, this ? this.lastID : null);
        });
    },
    read: (callback) => {
        const sql = 'SELECT * FROM categories';
        db.all(sql, [], (err, rows) => {
            callback(err, rows);
        });
    },
    update: (categoryId, name, description, callback) => {
        const sql = 'UPDATE categories SET name = ?, description = ? WHERE category_id = ?';
        db.run(sql, [name, description, categoryId], function(err) {
            callback(err, this.changes);
        });
    },
    delete: (categoryId, callback) => {
        const sql = 'DELETE FROM categories WHERE category_id = ?';
        db.run(sql, [categoryId], function(err) {
            callback(err, this.changes);
        });
    }
};

// CRUD operations for Posts
const postCRUD = {
    create: (title, content, author, categoryId, callback) => {
        const sql = 'INSERT INTO posts (title, content, author, date_created, category_id) VALUES (?, ?, ?, datetime(\'now\'), ?)';
        db.run(sql, [title, content, author, categoryId], function(err) {
            callback(err, this ? this.lastID : null);
        });
    },
    read: (callback) => {
        const sql = 'SELECT * FROM posts';
        db.all(sql, [], (err, rows) => {
            callback(err, rows);
        });
    },
    update: (postId, title, content, author, categoryId, callback) => {
        const sql = 'UPDATE posts SET title = ?, content = ?, author = ?, category_id = ? WHERE post_id = ?';
        db.run(sql, [title, content, author, categoryId, postId], function(err) {
            callback(err, this.changes);
        });
    },
    delete: (postId, callback) => {
        const sql = 'DELETE FROM posts WHERE post_id = ?';
        db.run(sql, [postId], function(err) {
            callback(err, this.changes);
        });
    }
};

// CRUD operations for Comments
const commentCRUD = {
    create: (postId, author, content, callback) => {
        const sql = 'INSERT INTO comments (post_id, author, content, date_created) VALUES (?, ?, ?, datetime(\'now\'))';
        db.run(sql, [postId, author, content], function(err) {
            callback(err, this ? this.lastID : null);
        });
    },
    read: (postId, callback) => {
        const sql = 'SELECT * FROM comments WHERE post_id = ?';
        db.all(sql, [postId], (err, rows) => {
            callback(err, rows);
        });
    },
    update: (commentId, content, callback) => {
        const sql = 'UPDATE comments SET content = ? WHERE comment_id = ?';
        db.run(sql, [content, commentId], function(err) {
            callback(err, this.changes);
        });
    },
    delete: (commentId, callback) => {
        const sql = 'DELETE FROM comments WHERE comment_id = ?';
        db.run(sql, [commentId], function(err) {
            callback(err, this.changes);
        });
    }
};

// Export the CRUD operations for use in other files
module.exports = {
    categoryCRUD,
    postCRUD,
    commentCRUD
};
