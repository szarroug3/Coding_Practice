// https://adventofcode.com/2020/day/3

const { readFile } = require('../utils/input');

async function partA(data, right, down) {
  return new Promise((resolve) => {
    let count = 0;
    let j = 0;
    for (let i = 0; i < data.length; i += down) {
      if (data[i][j] == '#') {
        count++;
      }

      j = (j + right) % data[i].length;
    }
    resolve(count);
  });
}

async function main() {
  try {
    var data = readFile('\n');
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let answers = await Promise.all([
    partA(data, 1, 1),
    partA(data, 3, 1),
    partA(data, 5, 1),
    partA(data, 7, 1),
    partA(data, 1, 2),
  ])
    .then((answers) => {
      console.log(`Part A: ${answers[1]}`);
      console.log(
        'Part B:',
        answers.reduce((a, b) => a * b)
      );
    })
    .catch(console.log);
}

main();
