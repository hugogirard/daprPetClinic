const Animal = require('./Animal');
const Owner = require('./Owner');

/**
 * Appointment Model
 */
class Appointment {
  /**
   * @param {string} id - Unique appointment ID
   * @param {Animal} animal - Animal object
   * @param {Owner} owner - Owner object
   * @param {string} appointmentDate - Date and time of appointment (ISO string)
   * @param {string} reason - Reason for visit
   * @param {string|null} notes - Additional notes
   * @param {string} createdAt - Creation timestamp (ISO string)
   */
  constructor(id, animal, owner, appointmentDate, reason, notes, createdAt) {
    this.id = id;
    this.animal = animal;
    this.owner = owner;
    this.appointmentDate = appointmentDate;
    this.reason = reason;
    this.notes = notes;
    this.createdAt = createdAt;
  }

  /**
   * Create Appointment from JSON object
   * @param {Object} json 
   * @returns {Appointment}
   */
  static fromJSON(json) {
    return new Appointment(
      json.id,
      Animal.fromJSON(json.animal),
      Owner.fromJSON(json.owner),
      json.appointmentDate,
      json.reason,
      json.notes || null,
      json.createdAt
    );
  }

  /**
   * Convert to plain object
   * @returns {Object}
   */
  toJSON() {
    return {
      id: this.id,
      animal: this.animal.toJSON(),
      owner: this.owner.toJSON(),
      appointmentDate: this.appointmentDate,
      reason: this.reason,
      notes: this.notes,
      createdAt: this.createdAt
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

module.exports = Appointment;
