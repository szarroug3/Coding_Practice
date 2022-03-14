#!/usr/bin/env node
// https://projecteuler.net/problem=19

let count = 0;
for (
  let date = new Date('January 1, 1901 00:00:00');
  date.getFullYear() < 2001;
  date.setMonth(date.getMonth() + 1)
) {
  if (date.getDay() == 0) {
    count++;
  }
}
console.log(count);
