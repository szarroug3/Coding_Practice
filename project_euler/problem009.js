#!/usr/bin/env node
// https://projecteuler.net/problem=9

function specialPythagoreanTriplet() {
  for (let i = 1; i < 999; i++) {
    for (let j = 1; j < 999; j++) {
      if (i + j > 999) {
        continue;
      }
      for (let k = 1; k < 999; k++) {
        if (i + j + k != 1000) {
          continue;
        }
        if (i * i + j * j == k * k) {
          return i * j * k;
        }
      }
    }
  }
}

console.log(specialPythagoreanTriplet());
