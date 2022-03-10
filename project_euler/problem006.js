#!/usr/bin/env node
// https://projecteuler.net/problem=6

let sumOfSquares = 0;
let sum = 0;

for (let i = 1; i < 101; i++) {
  sumOfSquares += i * i;
  sum += i;
}

console.log(sum * sum - sumOfSquares);
