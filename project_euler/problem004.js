#!/usr/bin/env node
// https://projecteuler.net/problem=4

function isPalindrome(x) {
  x = x.toString();
  for (let i = 0; i < Math.ceil(x.length / 2); i++) {
    if (x[i] != x[x.length - 1 - i]) {
      return false;
    }
  }
  return true;
}

function findLargestPalindrome() {
  let max = 0;
  for (let i = 999; i > 99; i--) {
    for (let j = 999; j > 99; j--) {
      value = i * j;
      if (isPalindrome(value) && value > max) {
        max = value;
      }
    }
  }
  return max;
}

console.log(findLargestPalindrome());
