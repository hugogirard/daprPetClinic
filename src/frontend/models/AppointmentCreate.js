const Animal = require('./Animal');
const Owner = require('./Owner');

/**
 * Appointment Create Model
 */
class AppointmentCreate {
  /**
   * @param {Animal} animal - Animal object
   * @param {Owner} owner - Owner object
   * @param {string} appointmentDate - Date and time of appointment (ISO string)
   * @param {string} reason - Reason for visit
   * @param {string|null} notes - Additional notes
   */
  constructor(animal, owner, appointmentDate, reason, notes = null) {
    this.animal = animal;
    this.owner = owner;
    this.appointmentDate = appointmentDate;
    this.reason = reason;
    this.notes = notes;
  }

  /**
   * Create AppointmentCreate from form data
   * @param {Object} formData 
   * @returns {AppointmentCreate}
   */
  static fromFormData(formData) {
    const animal = new Animal(
      formData.animalName,
      formData.animalType,
      formData.animalBreed || null,
      formData.animalAge ? parseInt(formData.animalAge) : null
    );

    const owner = new Owner(
      formData.ownerName,
      formData.ownerEmail,
      formData.ownerPhone
    );

    return new AppointmentCreate(
      animal,
      owner,
      formData.appointmentDate,
      formData.reason,
      formData.notes || null
    );
  }

  /**
   * Convert to plain object for API
   * @returns {Object}
   */
  toJSON() {
    return {
      animal: this.animal.toJSON(),
      owner: this.owner.toJSON(),
      appointmentDate: this.appointmentDate,
      reason: this.reason,
      notes: this.notes
    };
  }
}

module.exports = AppointmentCreate;
