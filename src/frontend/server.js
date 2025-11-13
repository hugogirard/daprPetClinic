const express = require('express');
const path = require('path');
const session = require('express-session');
const adminRoutes = require('./routes/admin');
const customerRoutes = require('./routes/customer');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Session middleware
app.use(session({
  secret: 'petclinic-secret-key',
  resave: false,
  saveUninitialized: false,
  cookie: { secure: false } // Set to true if using HTTPS
}));

// Set view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Login page
app.get('/', (req, res) => {
  if (req.session.userEmail) {
    if (req.session.userEmail === 'admin@petclinic.com') {
      return res.redirect('/admin');
    }
    return res.redirect('/dashboard');
  }
  res.render('login', { error: null });
});

// Login handler
app.post('/login', (req, res) => {
  const { email, password } = req.body;
  
  // Fake login - always succeeds if email and password are provided
  if (!email || !password) {
    return res.render('login', { error: 'Please provide email and password' });
  }

  req.session.userEmail = email;
  
  // Redirect based on user type
  if (email === 'admin@petclinic.com') {
    return res.redirect('/admin');
  }
  
  res.redirect('/dashboard');
});

// Logout
app.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/');
});

// Mount routes
app.use('/admin', adminRoutes);
app.use('/', customerRoutes);

// Start server
app.listen(PORT, () => {
  console.log(`Pet Clinic Frontend running on http://localhost:${PORT}`);
});
