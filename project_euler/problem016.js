#!/usr/bin/env node
// https://projecteuler.net/problem=16

const number = BigInt(2) ** BigInt(1000);
const string = number.toLocaleString('fullwide', { useGrouping: false });
let value = 0;
for (let i = 0; i < string.length; i++) {
  value += parseInt(string[i]);
}
console.log(value);
