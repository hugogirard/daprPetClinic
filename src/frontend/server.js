const express = require('express');
const path = require('path');
const session = require('express-session');
const PetClinicService = require('./services/PetClinicService');
const AppointmentCreate = require('./models/AppointmentCreate');
const AnimalType = require('./models/AnimalType');

const app = express();
const PORT = process.env.PORT || 3000;

// Initialize Pet Clinic Service with Dapr
const petClinicService = new PetClinicService();

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

// Authentication middleware
const requireAuth = (req, res, next) => {
  if (!req.session.userEmail) {
    return res.redirect('/');
  }
  next();
};

// Admin middleware
const requireAdmin = (req, res, next) => {
  if (!req.session.userEmail || req.session.userEmail !== 'admin@petclinic.com') {
    return res.redirect('/dashboard');
  }
  next();
};

// Routes

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

// Dashboard (regular users)
app.get('/dashboard', requireAuth, async (req, res) => {
  try {
    const appointments = await petClinicService.listAppointments(req.session.userEmail);
    res.render('dashboard', {
      userEmail: req.session.userEmail,
      appointments: appointments,
      toast: req.query.toast || null
    });
  } catch (error) {
    res.render('dashboard', {
      userEmail: req.session.userEmail,
      appointments: [],
      toast: null
    });
  }
});

// New appointment page
app.get('/appointment/new', requireAuth, (req, res) => {
  res.render('new-appointment', {
    userEmail: req.session.userEmail,
    animalTypes: AnimalType.getAll()
  });
});

// Create appointment
app.post('/appointment/create', requireAuth, async (req, res) => {
  try {
    const appointmentData = AppointmentCreate.fromFormData({
      ...req.body,
      ownerEmail: req.session.userEmail
    });
    
    await petClinicService.createAppointment(appointmentData);
    res.redirect('/dashboard?toast=success');
  } catch (error) {
    res.redirect('/appointment/new?toast=error');
  }
});

// Cancel appointment
app.post('/appointment/cancel/:id', requireAuth, async (req, res) => {
  try {
    await petClinicService.cancelAppointment(req.params.id);
    res.redirect('/dashboard?toast=cancelled');
  } catch (error) {
    res.redirect('/dashboard?toast=error');
  }
});

// Admin page
app.get('/admin', requireAdmin, (req, res) => {
  res.render('admin', {
    userEmail: req.session.userEmail,
    error: null,
    success: null
  });
});

// Charge appointment (admin only)
app.post('/appointment/charge', requireAdmin, async (req, res) => {
  try {
    const { appointmentId } = req.body;
    
    if (!appointmentId) {
      return res.render('admin', {
        userEmail: req.session.userEmail,
        error: 'Please provide an appointment ID',
        success: null
      });
    }
    
    await petClinicService.chargeAppointment(appointmentId);
    
    res.render('admin', {
      userEmail: req.session.userEmail,
      error: null,
      success: `Appointment ${appointmentId} charged successfully!`
    });
  } catch (error) {
    res.render('admin', {
      userEmail: req.session.userEmail,
      error: error.message,
      success: null
    });
  }
});

// View appointment details
app.get('/appointment/:id', requireAuth, async (req, res) => {
  try {
    const appointment = await petClinicService.getAppointment(req.params.id);
    res.render('appointment-detail', {
      userEmail: req.session.userEmail,
      appointment: appointment
    });
  } catch (error) {
    res.redirect('/dashboard');
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Pet Clinic Frontend running on http://localhost:${PORT}`);
});
