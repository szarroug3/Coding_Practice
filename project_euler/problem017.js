#!/usr/bin/env node
// https://projecteuler.net/problem=17

const nums = [
  'zero',
  'one',
  'two',
  'three',
  'four',
  'five',
  'six',
  'seven',
  'eight',
  'nine',
  'ten',
  'eleven',
  'twelve',
  'thirteen',
  'fourteen',
  'fifteen',
  'sixteen',
  'seventeen',
  'eighteen',
  'nineteen',
];

const tens = [
  'twenty',
  'thirty',
  'forty',
  'fifty',
  'sixty',
  'seventy',
  'eighty',
  'ninety',
];

function numberToWords(x) {
  if (x < 20) return nums[x];

  let number = x % 10;
  if (x < 100) {
    return tens[Math.floor(x / 10) - 2] + (number ? '-' + nums[number] : '');
  }

  number = x % 100;
  if (x < 1000) {
    return (
      nums[Math.floor(x / 100)] +
      ' hundred' +
      (number == 0 ? '' : ' and ' + numberToWords(number))
    );
  }

  number = x % 1000;
  return (
    numberToWords(Math.floor(x / 1000)) +
    ' thousand' +
    (number != 0 ? ' ' + numberToWords(number) : '')
  );
}

let count = 0;
for (let i = 1; i < 1001; i++) {
  let string = numberToWords(i).replace(/[\W-]/g, '');
  count += string.length;
}
console.log(count);
