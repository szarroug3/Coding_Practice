// https://adventofcode.com/2020/day/6

const { readFile } = require('../utils/input');

function parse(data) {
  let results = [];
  let curr = {};
  let person = 1;

  data.forEach((element) => {
    if (element == '') {
      curr['count'] = person - 1;
      results.push(curr);
      curr = {};
      person = 0;
    } else {
      for (let i = 0; i < element.length; i++) {
        if (element[i] in curr) {
          curr[element[i]].push(person);
        } else {
          curr[element[i]] = [person];
        }
      }
    }
    person++;
  });

  // push the last group because the loop won't do it
  curr['count'] = person - 1;
  results.push(curr);
  return results;
}

async function partA(data) {
  return new Promise((resolve) => {
    resolve(
      data.reduce((count, curr) => {
        return count + Object.keys(curr).length;
      }, 0)
    );
  });
}

async function partB(data) {
  return new Promise((resolve) => {
    resolve(
      data.reduce((count, curr) => {
        for (var property in curr) {
          if (property != 'count' && curr[property].length == curr['count']) {
            count += 1;
          }
        }
        return count;
      }, 0)
    );
  });
}

async function main() {
  try {
    var data = parse(readFile('\n'));
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
