#!/usr/bin/env node
// https://projecteuler.net/problem=2

let sum = 2;
let values = [1, 2];
while (values[1] < 4000000) {
  values.push(values[0] + values[1]);
  values.shift();
  if (values[1] % 2 == 0) {
    sum += values[1];
  }
}
console.log(sum);
