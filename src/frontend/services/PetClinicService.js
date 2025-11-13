const { DaprClient, HttpMethod } = require('@dapr/dapr');
const Appointment = require('../models/Appointment');
const AppointmentSummary = require('../models/AppointmentSummary');

/**
 * Pet Clinic Service - handles all API calls using Dapr Client
 */
class PetClinicService {
  /**
   * @param {string} appId - Dapr app ID for the backend service
   * @param {number} daprPort - Dapr sidecar port (default: 3500)
   */
  constructor() {
    this.daprClient = new DaprClient();
    this.appId = 'appointment-api';
  }

  /**
   * Create a new appointment
   * @param {AppointmentCreate} appointmentData 
   * @returns {Promise<Appointment>}
   */
  async createAppointment(appointmentData) {
    try {
      const response = await this.daprClient.invoker.invoke(
        this.appId,
        'appointment',
        HttpMethod.POST,
        appointmentData.toJSON()
      );
      return Appointment.fromJSON(response);
    } catch (error) {
      console.error('Error creating appointment:', error);
      throw new Error(`Failed to create appointment: ${error.message}`);
    }
  }

  /**
   * List appointments by owner email
   * @param {string} ownerEmail 
   * @returns {Promise<AppointmentSummary[]>}
   */
  async listAppointments(ownerEmail) {
    try {
      const response = await this.daprClient.invoker.invoke(
        this.appId,
        `appointments/email/${encodeURIComponent(ownerEmail)}`,
        HttpMethod.GET
      );
      return response.map(item => AppointmentSummary.fromJSON(item));
    } catch (error) {
      console.error('Error listing appointments:', error);
      throw new Error(`Failed to list appointments: ${error.message}`);
    }
  }

  /**
   * Get a specific appointment by ID
   * @param {string} appointmentId 
   * @returns {Promise<Appointment>}
   */
  async getAppointment(appointmentId) {
    try {
      const response = await this.daprClient.invoker.invoke(
        this.appId,
        `appointments/byId/${appointmentId}`,
        HttpMethod.GET
      );
      return Appointment.fromJSON(response);
    } catch (error) {
      console.error('Error getting appointment:', error);
      throw new Error(`Failed to get appointment: ${error.message}`);
    }
  }

  /**
   * Charge an appointment (admin only)
   * @param {string} appointmentId 
   * @returns {Promise<void>}
   */
  async chargeAppointment(appointmentId) {
    try {
      await this.daprClient.invoker.invoke(
        this.appId,
        `appointment/charge/${appointmentId}`,
        HttpMethod.POST
      );
    } catch (error) {
      console.error('Error charging appointment:', error);
      throw new Error(`Failed to charge appointment: ${error.message}`);
    }
  }

  /**
   * Cancel an appointment
   * @param {string} appointmentId 
   * @returns {Promise<void>}
   */
  async cancelAppointment(appointmentId) {
    try {
      await this.daprClient.invoker.invoke(
        this.appId,
        `appointments/${appointmentId}`,
        HttpMethod.DELETE
      );
    } catch (error) {
      console.error('Error canceling appointment:', error);
      throw new Error(`Failed to cancel appointment: ${error.message}`);
    }
  }
}

module.exports = PetClinicService;
