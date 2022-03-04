// https://adventofcode.com/2020/day/#

const { readFile } = require('../utils/input');

function onResolve(results) {}

async function partA(data) {
  return new Promise((resolve, reject) => {
    reject('UPDATE THIS');
  });
}

async function partB(data) {
  return new Promise((resolve, reject) => {
    resolve('UPDATE THIS');
  });
}

async function main() {
  try {
    var data = readFile();
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