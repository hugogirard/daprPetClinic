const express = require('express');
const router = express.Router();
const PetClinicService = require('../services/PetClinicService');

// Initialize Pet Clinic Service with Dapr
const petClinicService = new PetClinicService();

// Admin middleware
const requireAdmin = (req, res, next) => {
  if (!req.session.userEmail || req.session.userEmail !== 'admin@petclinic.com') {
    return res.redirect('/dashboard');
  }
  next();
};

// Admin page
router.get('/', requireAdmin, (req, res) => {
  res.render('admin', {
    userEmail: req.session.userEmail,
    error: null,
    success: null
  });
});

// Search appointments by email (admin only)
router.get('/search', requireAdmin, async (req, res) => {
  try {
    const email = req.query.email;
    if (!email) {
      return res.json({ success: false, error: 'Email is required' });
    }
    
    const appointments = await petClinicService.listAppointments(email);
    
    // Get full appointment details for each
    const detailedAppointments = await Promise.all(
      appointments.map(async (summary) => {
        try {
          return await petClinicService.getAppointment(summary.id);
        } catch (err) {
          console.warn(`Could not fetch appointment ${summary.id}:`, err.message);
          return null;
        }
      })
    );
    
    // Filter out nulls from failed fetches
    const validAppointments = detailedAppointments.filter(a => a !== null);
    
    res.json({ 
      success: true, 
      appointments: validAppointments
    });
  } catch (error) {
    console.error('Search error:', error);
    res.json({ success: false, error: error.message });
  }
});

// Charge appointment (admin only)
router.post('/charge', requireAdmin, async (req, res) => {
  try {
    const { appointmentId } = req.body;
    
    if (!appointmentId) {
      req.session.flash = { type: 'error', message: 'Please provide an appointment ID' };
      return res.redirect('/admin');
    }
    
    await petClinicService.chargeAppointment(appointmentId);
    req.session.flash = { type: 'success', message: 'Appointment charged successfully' };
    res.redirect('/admin');
  } catch (error) {
    req.session.flash = { type: 'error', message: `Failed to charge appointment: ${error.message}` };
    res.redirect('/admin');
  }
});

module.exports = router;
