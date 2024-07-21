const express = require('express');
const db = require('../crud/blog_crud');
const { isAuthenticated, isAdmin } = require('../middleware/auth');

const router = express.Router();

router.get('/create-post', isAuthenticated, isAdmin, (req, res) => {
    res.render('pages/create_post');
});

// Route to create a new post
router.post('/create-post', isAuthenticated, isAdmin, async (req, res) => {
    const { title, content, author, categoryId } = req.body;

    // Validate input (basic validation example)
    if (!title || !content || !author || !categoryId) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    // Call create method from postCRUD
    db.postCRUD.create(title, content, author, categoryId, (err, postId) => {
        if (err) {
            return res.status(500).json({ error: 'Failed to create post' });
        }
        res.redirect('/get-all-posts');
    });
});

// Get All Posts Endpoint
router.get('/get-all-posts', isAuthenticated, isAdmin, async (req, res) => {
    db.postCRUD.readAll((err, posts) => {
        if (err) {
            console.error('Error fetching posts:', err.message);
            res.status(500).send('Error fetching posts');
        } else {
            res.render('pages/all_post', { posts });
        }
    });
});

// Route to delete a post
router.post('/delete-post/:id', isAuthenticated, isAdmin, (req, res) => {
    const postId = req.params.id;

    db.postCRUD.delete(postId, (err) => {
        if (err) {
            console.error('Error deleting post:', err.message);
            return res.status(500).json({ error: 'Failed to delete post' });
        }
        res.redirect('/get-all-posts');
    });
});

// Route to render the update post page
router.get('/update-post/:id', isAuthenticated, isAdmin, async (req, res) => {
    const postId = req.params.id;

    db.postCRUD.read(postId, (err, post) => {
        if (err) {
            console.error('Error fetching post:', err.message);
            return res.status(500).json({ error: 'Failed to fetch post' });
        }
        res.render('pages/update_post', { post });
    });
});

// Route to update a post
router.post('/update-post/:id', isAuthenticated, isAdmin, async (req, res) => {
    const postId = req.params.id;
    const { title, content, author, categoryId } = req.body;

    // Validate input (basic validation example)
    if (!title || !content || !author || !categoryId) {
        return res.status(400).json({ error: 'All fields are required' });
    }

    db.postCRUD.update(postId, title, content, author, categoryId, (err) => {
        if (err) {
            console.error('Error updating post:', err.message);
            return res.status(500).json({ error: 'Failed to update post' });
        }
        res.redirect('/get-all-posts');
    });
});

module.exports = router;
