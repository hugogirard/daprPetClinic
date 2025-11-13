const express = require('express');
const router = express.Router();

// Login page
router.get('/', (req, res) => {
  if (req.session.userEmail) {
    if (req.session.userEmail === 'admin@petclinic.com') {
      return res.redirect('/admin');
    }
    return res.redirect('/dashboard');
  }
  res.render('login', { error: null });
});

// Login handler
router.post('/login', (req, res) => {
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
router.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/');
});

module.exports = router;
