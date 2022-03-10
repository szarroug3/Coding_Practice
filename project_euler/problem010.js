#!/usr/bin/env node
// https://projecteuler.net/problem=10

const { isPrime } = require('./utils');

let sum = 0;
for (let curr = 2; curr < 2000000; curr++) {
  if (isPrime(curr)) {
    sum += curr;
  }
}
console.log(sum);
