const express = require('express');
const bcrypt = require('bcryptjs');
const db = require('../crud/auth_crud'); 

const router = express.Router();

// Middleware to check if the user is authenticated
function isAuthenticated(req, res, next) {
    if (req.session && req.session.user) {
        return next();
    } else {
        res.redirect('/login');
    }
}

// Middleware to check if the user is an admin
function isAdmin(req, res, next) {
    if (req.session && req.session.user && req.session.user.is_admin === 1) {
        return next();
    } else {
        res.status(403).send('Access denied');
    }
}

// Register Page
router.get('/register', (req, res) => {
    res.render('pages/register');
});

// Login Page
router.get('/login', (req, res) => {
    res.render('pages/login');
});

// Protect the /admin endpoint
router.get('/admin', isAuthenticated, isAdmin, (req, res) => {
    res.render('pages/admin');
});


// Register User
router.post('/register', async (req, res) => {
    const { username, password, email } = req.body;
    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const is_admin = 0;
        db.createUser(username, hashedPassword, email, is_admin, (err, userId) => {
            if (err) {
                console.error('Error creating user:', err.message);
                res.status(500).send('Error creating user');
            } else {
                res.redirect('/login');
            }
        });
    } catch (error) {
        console.error('Error hashing password:', error.message);
        res.status(500).send('Internal Server Error');
    }
});

router.post('/login', (req, res) => {
    const { username, password } = req.body;
    db.getUser(username, async (err, user) => {
        try {
            if (err || !user) {
                console.error('User not found:', err ? err.message : 'No user');
                res.status(401).send('Invalid credentials');
                return;
            }
            
            const isMatch = await bcrypt.compare(password, user.password);
            if (!isMatch) {
                console.error('Password mismatch');
                res.status(401).send('Invalid credentials');
                return;
            }

            // Passwords match, store user info in session
            req.session.user = {
                id: user.user_id,
                username: user.username,
                is_admin: user.is_admin
            };

            // Redirect based on admin status
            if (user.is_admin === 1) {
                res.redirect('/admin');
            } else {
                res.redirect('/');
            }
        } catch (error) {
            console.error('Error comparing passwords:', error.message);
            res.status(500).send('Internal Server Error');
        }
    });
});

// Logout User
router.get('/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            console.error('Error destroying session:', err.message);
            res.status(500).send('Unable to log out');
        } else {
            res.redirect('/login');
        }
    });
});


module.exports = router;
