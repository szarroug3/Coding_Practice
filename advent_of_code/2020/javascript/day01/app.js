// https://adventofcode.com/2020/day/1

const { readFile } = require('../utils/input');

async function partA(data) {
  return new Promise((resolve, reject) => {
    for (let i = 0; i < data.length - 1; i++) {
      for (let j = i + 1; j < data.length; j++) {
        if (data[i] + data[j] == 2020) {
          resolve(data[i] * data[j]);
        }
      }
    }
    reject('Part A: No answer found');
  });
}

async function partB(data) {
  return new Promise((resolve, reject) => {
    for (let i = 0; i < data.length - 2; i++) {
      for (let j = i + 1; j < data.length - 1; j++) {
        for (let k = j + 1; k < data.length; k++) {
          if (data[i] + data[j] + data[k] == 2020) {
            resolve(data[i] * data[j] * data[k]);
          }
        }
      }
    }
    reject('Part B: No answer found');
  });
}

async function main() {
  try {
    var data = readFile('\n', Number);
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  answers = await Promise.all([partA(data), partB(data)])
    .then((answers) => {
      console.log(`Part A: ${answers[0]}`);
      console.log(`Part B: ${answers[1]}`);
    })
    .catch(console.log);
}

main();
