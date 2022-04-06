// https://adventofcode.com/2020/day/18

const exp = require('constants');
const { readFile } = require('../utils/input');

async function partA(data) {
  return new Promise((resolve) => {
    let sum = 0;
    data.forEach((expression) => {
      expression = evaluateParentheses(expression);
      let evaluated = evaluate(expression);
      sum += evaluated;
    });
    resolve(sum);
  });
}

function evaluateParentheses(expression) {
  let re = /\(([0-9 +*]+)\)/;
  while (expression.includes('(')) {
    let match = expression.match(re);
    expression = expression.replace(match[0], evaluate(match[1]));
  }
  return expression;
}

function evaluate(expression) {
  let splitExpression = expression.split(' ');
  if (splitExpression.length == 1) {
    return parseInt(splitExpression[0]);
  }

  let values = [
    splitExpression[1] === '*'
      ? parseInt(splitExpression[0]) * parseInt(splitExpression[2])
      : parseInt(splitExpression[0]) + parseInt(splitExpression[2]),
  ];
  values.push(...splitExpression.slice(3));
  return evaluate(values.join(' '));
}

async function partB(data) {
  return new Promise((resolve) => {
    resolve('UPDATE THIS');
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
