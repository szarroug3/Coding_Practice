#!/usr/bin/env node
// https://projecteuler.net/problem=15

const { factorial } = require('./utils');

function countPaths(i, j) {
  return Math.floor(factorial(i + j) / (factorial(i) * factorial(j)));
}

console.log(countPaths(20, 20));
