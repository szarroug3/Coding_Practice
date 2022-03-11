#!/usr/bin/env node
// https://projecteuler.net/problem=14

function collatz(x) {
  let values = [x];
  let curr = x;

  while (curr != 1) {
    if (curr % 2 == 0) {
      curr = curr / 2;
    } else {
      curr = 3 * curr + 1;
    }
    values.push(curr);
  }

  return values;
}

let longest = 1;
let value = 1;
for (let i = 1; i < 1000000; i++) {
  values = collatz(i);
  if (values.length > longest) {
    longest = values.length;
    value = i;
  }
}
console.log(value);
