// https://adventofcode.com/2020/day/11

const { readFile } = require('../utils/input');

async function partA(data) {
  return new Promise((resolve) => {
    let old = [];
    let curr = data.slice();
    while (!areArraysEqual(old, curr)) {
      old = curr.slice();
      curr = getSeats(curr, countImmediateSurrounding, 4);
    }

    let count = curr.reduce((count, row) => {
      return (
        count +
        row.reduce(
          (rowCount, seat) => (seat == '#' ? rowCount + 1 : rowCount),
          0
        )
      );
    }, 0);

    resolve(count);
  });
}

function areArraysEqual(a, b) {
  if (a.length != b.length) {
    return false;
  }

  for (let i = 0; i < a.length; i++) {
    if (a[i].length != b[i].length) {
      return false;
    }
    for (let j = 0; j < a[i].length; j++) {
      if (a[i][j] != b[i][j]) {
        return false;
      }
    }
  }
  return true;
}

function getSeats(data, countSurroundingFunc, occupiedCount) {
  let seats = [];
  for (let i = 0; i < data.length; i++) {
    let curr = [];
    for (let j = 0; j < data[i].length; j++) {
      if (data[i][j] == '.') {
        curr.push('.');
        continue;
      }

      count = countSurroundingFunc(data, i, j);
      if (data[i][j] == 'L' && count == 0) {
        curr.push('#');
      } else if (data[i][j] == '#' && count >= occupiedCount) {
        curr.push('L');
      } else {
        curr.push(data[i][j]);
      }
    }
    seats.push(curr);
  }
  return seats;
}

function countImmediateSurrounding(data, row, column) {
  let count = 0;
  for (let i = row - 1; i < row + 2; i++) {
    if (i < 0 || i >= data.length) {
      continue;
    }

    for (let j = column - 1; j < column + 2; j++) {
      if (j < 0 || j >= data[i].length) {
        continue;
      }
      if (i == row && j == column) {
        continue;
      }
      if (data[i][j] == '#') {
        count++;
      }
    }
  }
  return count;
}

async function partB(data) {
  return new Promise((resolve) => {
    let old = [];
    let curr = data.slice();
    while (!areArraysEqual(old, curr)) {
      old = curr.slice();
      curr = getSeats(curr, countSurrounding, 5);
    }

    let count = curr.reduce((count, row) => {
      return (
        count +
        row.reduce(
          (rowCount, seat) => (seat == '#' ? rowCount + 1 : rowCount),
          0
        )
      );
    }, 0);

    resolve(count);
  });
}

function countSurrounding(data, row, column) {
  let count = 0;

  // diagonally up to the left
  let i = row - 1;
  let j = column - 1;
  while (i >= 0 && j >= 0 && data[i][j] == '.') {
    i--;
    j--;
  }
  if (i >= 0 && j >= 0 && data[i][j] == '#') {
    count++;
  }

  // straight up
  i = row - 1;
  j = column;
  while (i >= 0 && data[i][j] == '.') {
    i--;
  }
  if (i >= 0 && data[i][j] == '#') {
    count++;
  }

  // diagonally up to the right
  i = row - 1;
  j = column + 1;
  while (i >= 0 && j < data[i].length && data[i][j] == '.') {
    i--;
    j++;
  }
  if (i >= 0 && j < data[i].length && data[i][j] == '#') {
    count++;
  }

  // straight right
  i = row;
  j = column + 1;
  while (j < data[i].length && data[i][j] == '.') {
    j++;
  }
  if (j < data[i].length && data[i][j] == '#') {
    count++;
  }

  // diagonally down to the right
  i = row + 1;
  j = column + 1;
  while (i < data.length && j < data[i].length && data[i][j] == '.') {
    i++;
    j++;
  }
  if (i < data.length && j < data[i].length && data[i][j] == '#') {
    count++;
  }

  // straight down
  i = row + 1;
  j = column;
  while (i < data.length && data[i][j] == '.') {
    i++;
  }
  if (i < data.length && data[i][j] == '#') {
    count++;
  }

  // diagonally down to the left
  i = row + 1;
  j = column - 1;
  while (i < data.length && j >= 0 && data[i][j] == '.') {
    i++;
    j--;
  }
  if (i < data.length && j >= 0 && data[i][j] == '#') {
    count++;
  }

  // straight left
  i = row;
  j = column - 1;
  while (i >= 0 && data[i][j] == '.') {
    j--;
  }
  if (i >= 0 && data[i][j] == '#') {
    count++;
  }

  return count;
}

async function main() {
  try {
    var data = readFile('\n', null, '');
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
