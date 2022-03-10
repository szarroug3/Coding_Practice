#!/usr/bin/env node
// https://projecteuler.net/problem=5

function smallestMultiple() {
  let found = false;
  let value = 20;
  for (; !found; value++) {
    found = true;
    // we only need to check 11-20 because every number
    // below that is already covered by these numbers
    for (let i = 20; i > 10; i--) {
      if (value % i != 0) {
        found = false;
        break;
      }
    }
  }
  return value - 1;
}

console.log(smallestMultiple());
