// https://adventofcode.com/2020/day/13

const { readFile } = require('../utils/input');

function parse(data) {
  let buses = [];
  data[1].split(',').forEach((element) => {
    if (isNaN(element)) {
      buses.push(element);
    } else {
      buses.push(parseInt(element));
    }
  });
  return [parseInt(data[0]), buses];
}

async function partA(data) {
  return new Promise((resolve) => {
    for (let curr = data[0]; true; curr++) {
      for (let i = 0; i < data[1].length; i++) {
        if (curr % data[1][i] == 0) {
          resolve(data[1][i] * (curr - data[0]));
          return;
        }
      }
    }
  });
}

async function partB(data) {
  return new Promise((resolve) => {
    let timeDelta = 1;
    let time = 0;

    for (let i = 0; i < data.length; i++) {
      if (data[i] == 'x') {
        continue;
      }
      while (true) {
        time += timeDelta;
        if ((time + i) % data[i] == 0) {
          timeDelta *= data[i];
          break;
        }
      }
    }
    resolve(time);
  });
}

async function main() {
  try {
    var data = parse(readFile('\n'));
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let answers = await Promise.all([partA(data), partB(data[1])])
    .then((answers) => {
      console.log(`Part A: ${answers[0]}`);
      console.log(`Part B: ${answers[1]}`);
    })
    .catch(console.log);
}

main();
