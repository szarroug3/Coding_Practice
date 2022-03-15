// https://adventofcode.com/2020/day/5

const { resolve } = require('path');
const { readFile } = require('../utils/input');

function getLocation(curr, min, max) {
  let halfway = Math.ceil((max - min) / 2);
  if (curr == 'F' || curr == 'L') {
    max -= halfway;
  } else {
    min += halfway;
  }

  return [min, max];
}

function getSeat(curr) {
  let row = 0;
  let max = 127;
  for (let i = 0; i < 7; i++) {
    values = getLocation(curr[i], row, max);
    row = values[0];
    max = values[1];
  }

  let column = 0;
  max = 7;
  for (let i = 7; i < 10; i++) {
    values = getLocation(curr[i], column, max);
    column = values[0];
    max = values[1];
  }

  return row * 8 + column;
}

async function partA(data) {
  return new Promise((resolve) => {
    let highest = 0;
    data.forEach((element) => {
      let seatID = getSeat(element);
      if (seatID > highest) {
        highest = seatID;
      }
    });
    resolve(highest);
  });
}

async function partB(data) {
  return new Promise((resolve, reject) => {
    let values = [];
    data.forEach((element) => values.push(getSeat(element)));
    values.sort();
    for (let i = 0; i < values.length - 1; i++) {
      if (values[i] == values[i + 1] - 2) {
        resolve(values[i] + 1);
      }
    }
    reject("Couldn't find seat.");
  });
}

async function main() {
  try {
    var data = readFile('\n');
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let answers = await Promise.all([partA(data), partB(data)])
    .then((answers) => {
      console.log(`Part A: ${answers[0]}`);
      console.log(`Part B: ${answers[1]}`);
    })
    .catch(console.log);
}

main();
