#!/usr/bin/env node
// https://projecteuler.net/problem=7

const { isPrime } = require('./utils');

let curr = 2;
for (let count = 0; count < 10001; curr++) {
  if (isPrime(curr)) {
    count++;
  }
}
console.log(curr - 1);
