const express = require('express');
const router = express.Router();
const PetClinicService = require('../services/PetClinicService');
const AppointmentCreate = require('../models/AppointmentCreate');
const AnimalType = require('../models/AnimalType');

// Initialize Pet Clinic Service with Dapr
const petClinicService = new PetClinicService();

// Authentication middleware
const requireAuth = (req, res, next) => {
  if (!req.session.userEmail) {
    return res.redirect('/');
  }
  next();
};

// Dashboard (regular users)
router.get('/dashboard', requireAuth, async (req, res) => {
  try {
    const appointments = await petClinicService.listAppointments(req.session.userEmail);
    res.render('dashboard', {
      userEmail: req.session.userEmail,
      appointments: appointments
    });
  } catch (error) {
    res.render('dashboard', {
      userEmail: req.session.userEmail,
      appointments: []
    });
  }
});

// New appointment page
router.get('/appointment/new', requireAuth, (req, res) => {
  res.render('new-appointment', {
    userEmail: req.session.userEmail,
    animalTypes: AnimalType.getAll()
  });
});

// Create appointment
router.post('/appointment/create', requireAuth, async (req, res) => {
  try {
    const appointmentData = AppointmentCreate.fromFormData({
      ...req.body,
      ownerEmail: req.session.userEmail
    });
    
    await petClinicService.createAppointment(appointmentData);
    req.session.flash = { type: 'success', message: 'Appointment created successfully!' };
    res.redirect('/dashboard');
  } catch (error) {
    req.session.flash = { type: 'error', message: `Failed to create appointment: ${error.message}` };
    res.redirect('/appointment/new');
  }
});

// Cancel appointment
router.post('/appointment/cancel/:id', requireAuth, async (req, res) => {
  try {
    await petClinicService.cancelAppointment(req.params.id);
    req.session.flash = { type: 'cancelled', message: 'Appointment cancelled successfully' };
    res.redirect('/dashboard');
  } catch (error) {
    req.session.flash = { type: 'error', message: `Failed to cancel appointment: ${error.message}` };
    res.redirect('/dashboard');
  }
});

// View appointment details
router.get('/appointment/:id', requireAuth, async (req, res) => {
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

module.exports = router;
