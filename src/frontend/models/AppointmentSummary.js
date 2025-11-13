/**
 * Appointment Summary Model
 */
class AppointmentSummary {
  /**
   * @param {string} id - Appointment ID
   * @param {string} appointmentDate - Date and time of appointment (ISO string)
   */
  constructor(id, appointmentDate) {
    this.id = id;
    this.appointmentDate = appointmentDate;
  }

  /**
   * Create AppointmentSummary from JSON object
   * @param {Object} json 
   * @returns {AppointmentSummary}
   */
  static fromJSON(json) {
    return new AppointmentSummary(
      json.id,
      json.appointmentDate
    );
  }

  /**
   * Convert to plain object
   * @returns {Object}
   */
  toJSON() {
    return {
      id: this.id,
      appointmentDate: this.appointmentDate
    };
  }

  /**
   * Get formatted appointment date
   * @returns {string}
   */
  getFormattedDate() {
    return new Date(this.appointmentDate).toLocaleString();
  }
}

module.exports = AppointmentSummary;
