/**
 * Owner Model
 */
class Owner {
  /**
   * @param {string} name - Owner's full name
   * @param {string} email - Owner's email
   * @param {string} phone - Owner's phone number
   */
  constructor(name, email, phone) {
    this.name = name;
    this.email = email;
    this.phone = phone;
  }

  /**
   * Create Owner from JSON object
   * @param {Object} json 
   * @returns {Owner}
   */
  static fromJSON(json) {
    return new Owner(
      json.name,
      json.email,
      json.phone
    );
  }

  /**
   * Convert to plain object
   * @returns {Object}
   */
  toJSON() {
    return {
      name: this.name,
      email: this.email,
      phone: this.phone
    };
  }
}

module.exports = Owner;
