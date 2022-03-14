#!/usr/bin/env node
// https://projecteuler.net/problem=20

const { getFactorial } = require('./utils');

let factorial = getFactorial(100);
const string = factorial.toLocaleString('fullwide', { useGrouping: false });

let sum = 0;
for (let i = 0; i < string.length; i++) {
  sum += parseInt(string[i]);
}

console.log(sum);
