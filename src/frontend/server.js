const express = require('express');
const path = require('path');
const session = require('express-session');
const loginRoutes = require('./routes/login');
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

// Mount routes
app.use('/', loginRoutes);
app.use('/admin', adminRoutes);
app.use('/', customerRoutes);

// Start server
app.listen(PORT, () => {
  console.log(`Pet Clinic Frontend running on http://localhost:${PORT}`);
});
