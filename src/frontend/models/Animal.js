/**
 * Animal Model
 */
class Animal {
  /**
   * @param {string} name - Name of the animal
   * @param {string} type - Type of animal (dog, cat, bird, etc.)
   * @param {string|null} breed - Breed of the animal
   * @param {number|null} age - Age in years
   */
  constructor(name, type, breed = null, age = null) {
    this.name = name;
    this.type = type;
    this.breed = breed;
    this.age = age;
  }

  /**
   * Create Animal from JSON object
   * @param {Object} json 
   * @returns {Animal}
   */
  static fromJSON(json) {
    return new Animal(
      json.name,
      json.type,
      json.breed || null,
      json.age || null
    );
  }

  /**
   * Convert to plain object
   * @returns {Object}
   */
  toJSON() {
    return {
      name: this.name,
      type: this.type,
      breed: this.breed,
      age: this.age
    };
  }
}

module.exports = Animal;
