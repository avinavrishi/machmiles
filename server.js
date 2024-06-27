const express = require('express');
const session = require('express-session');
const path = require('path');
const dotenv = require('dotenv');
const authRoutes = require('./router/auth');
const agodaRoutes = require('./router/agoda');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Session configuration
app.use(session({
  secret: process.env.SESSION_KEY,
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false } // Set to true if using HTTPS
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));

// Use Routes
app.use('/', authRoutes);
app.use('/',agodaRoutes);

// Endpoint to serve the sitemap
app.get('/sitemap.xml', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'sitemap.xml'));
});

app.get('/', (req, res) => {
  res.render('pages/index');
});


app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
