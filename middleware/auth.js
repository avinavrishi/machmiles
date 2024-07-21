// middleware/auth.js

function isAuthenticated(req, res, next) {
    if (req.session && req.session.user) {
        return next();
    } else {
        res.redirect('/login');
    }
}

function isAdmin(req, res, next) {
    if (req.session && req.session.user && req.session.user.is_admin === 1) {
        return next();
    } else {
        res.status(403).send('Access denied');
    }
}

module.exports = {
    isAuthenticated,
    isAdmin
};
