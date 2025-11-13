/**
 * Animal Type Enum
 */
class AnimalType {
  static DOG = 'dog';
  static CAT = 'cat';
  static BIRD = 'bird';
  static RABBIT = 'rabbit';
  static HAMSTER = 'hamster';
  static OTHER = 'other';

  static getAll() {
    return [
      AnimalType.DOG,
      AnimalType.CAT,
      AnimalType.BIRD,
      AnimalType.RABBIT,
      AnimalType.HAMSTER,
      AnimalType.OTHER
    ];
  }
}

module.exports = AnimalType;
