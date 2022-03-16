// https://adventofcode.com/2020/day/8

const { readFile } = require('../utils/input');
const func = {
  acc: acc,
  jmp: jmp,
  nop: nop,
};

function acc(argument, accumulator, index) {
  accumulator += argument;
  index++;
  return [accumulator, index];
}

function jmp(argument, accumulator, index) {
  index += argument;
  return [accumulator, index];
}

function nop(_, accumulator, index) {
  index++;
  return [accumulator, index];
}

function runCode(data, fixIndex, fixFunc) {
  let accumulator = 0;
  let index = 0;
  let visited = [];
  let repeated = false;

  for (; index < data.length; ) {
    if (visited.includes(index)) {
      repeated = true;
      break;
    }

    let currFunc = data[index][0];
    if (fixIndex == index) {
      currFunc = fixFunc;
    }

    visited.push(index);
    let values = currFunc(data[index][1], accumulator, index);
    accumulator = values[0];
    index = values[1];
  }

  return [accumulator, repeated];
}

function findNextPossiblyCorrupt(data, start) {
  for (let i = start + 1; start < data.length; i++) {
    if (data[i][0] == jmp) {
      return [i, nop];
    }
    if (data[i][0] == nop) {
      return [i, nop];
    }
  }
}

async function partA(data) {
  return new Promise((resolve) => {
    let results = runCode(data);
    resolve(results[0]);
  });
}

async function partB(data) {
  return new Promise((resolve) => {
    let results = [null, true];
    let index = -1;

    while (results[1]) {
      let nextCorrupt = findNextPossiblyCorrupt(data, index);
      results = runCode(data, nextCorrupt[0], nextCorrupt[1]);
      index = nextCorrupt[0];
    }
    resolve(results[0]);
  });
}

async function main() {
  try {
    var data = readFile('\n', null, ' ', (value) =>
      isNaN(value) ? func[value] : parseInt(value)
    );
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
