#!/usr/bin/env node
// https://projecteuler.net/problem=3

function findFactors(value) {
  for (let i = 2; i < value / 2; i++) {
    if (value % i == 0) {
      return [i, value / i];
    }
  }
  return [];
}

function findPrimeFactors(value) {
  let values = findFactors(value);
  let complete = [];

  while (values.length > 0) {
    let curr = [];
    values = values.forEach((element) => {
      factors = findFactors(element);
      if (factors.length == 0) {
        complete.push(element);
      } else {
        factors.forEach((factor) => {
          curr.push(factor);
        });
      }
    });
    values = curr;
  }

  return complete;
}

function getLargestPrimeFactor(value) {
  factors = findPrimeFactors(value);
  if (factors.length == 0) {
    throw new Error('Could not find factors.');
  }

  factors.sort((a, b) => {
    return a > b;
  });

  return factors[factors.length - 1];
}

try {
  console.log(getLargestPrimeFactor(600851475143));
} catch (e) {
  console.log(e.message);
}
