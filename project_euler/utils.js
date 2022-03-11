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
