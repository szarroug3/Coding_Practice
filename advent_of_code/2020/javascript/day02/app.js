// https://adventofcode.com/2020/day/2

const { readFile } = require('../utils/input');

async function partA(data) {
  return new Promise((resolve) => {
    let count = 0;
    data.forEach((element) => {
      let matches = element.match(/(\d+)-(\d+) (.*): (.*)/);
      let min = parseInt(matches[1]);
      let max = parseInt(matches[2]);
      let letter = matches[3];
      let password = matches[4];

      let result = password.match(new RegExp(`${letter}`, 'g'));
      if (result == null) {
        return;
      }
      if (result.length >= min && result.length <= max) {
        count++;
      }
    });
    resolve(count);
  });
}

async function partB(data) {
  return new Promise((resolve) => {
    let count = 0;
    data.forEach((element) => {
      let matches = element.match(/(\d+)-(\d+) (.*): (.*)/);
      let first = parseInt(matches[1]);
      let second = parseInt(matches[2]);
      let letter = matches[3];
      let password = matches[4];

      // this is ternary operator that implements a logical XOR
      if (
        password[first - 1] == letter
          ? password[second - 1] != letter
          : password[second - 1] == letter
      ) {
        count++;
      }
    });
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

  let answers = await Promise.all([partA(data), partB(data)])
    .then((answers) => {
      console.log(`Part A: ${answers[0]}`);
      console.log(`Part B: ${answers[1]}`);
    })
    .catch(console.log);
}

main();
