module.exports.isPrime = (x) => {
  for (let i = 2; i <= Math.ceil(x / 2); i++) {
    if (x % i == 0) {
      return false;
    }
  }
  return true;
};

module.exports.findFactors = (x) => {
  values = [];
  for (let i = 1; i <= Math.floor(Math.sqrt(x)); i++) {
    if (x % i == 0) {
      values.push(i);
      if (x / i != i) {
        values.push(x / i);
      }
    }
  }
  return values;
};

module.exports.getFactorial = (x) => {
  let value = BigInt(2);
  for (let i = 3; i <= x; i++) {
    value *= BigInt(i);
  }
  return value;
};
