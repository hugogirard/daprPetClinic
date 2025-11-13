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
          return null;
        }
      })
    );
    
    res.json({ 
      success: true, 
      appointments: detailedAppointments.filter(a => a !== null) 
    });
  } catch (error) {
    res.json({ success: false, error: error.message });
  }
});

// Charge appointment (admin only)
router.post('/appointment/charge', requireAdmin, async (req, res) => {
  try {
    const { appointmentId } = req.body;
    
    if (!appointmentId) {
      return res.redirect('/admin?toast=error&message=Please+provide+an+appointment+ID');
    }
    
    await petClinicService.chargeAppointment(appointmentId);
    res.redirect('/admin?toast=success&message=Appointment+charged+successfully');
  } catch (error) {
    res.redirect('/admin?toast=error&message=' + encodeURIComponent(error.message));
  }
});

module.exports = router;
