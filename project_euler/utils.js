function isPrime(x) {
  for (let i = 2; i <= Math.ceil(x / 2); i++) {
    if (x % i == 0) {
      return false;
    }
  }
  return true;
}

module.exports = { isPrime };
