#!/usr/bin/env node
// https://projecteuler.net/problem=12

const { findFactors } = require('./utils');

let curr = 0;
let values = [];
let i = 1;
for (; values.length < 501; i++) {
  curr += i;
  values = findFactors(curr);
}
console.log(curr);
