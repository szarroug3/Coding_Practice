// https://adventofcode.com/2020/day/10

const { builtinModules } = require('module');
const { posix } = require('path');
const { readFile } = require('../utils/input');

async function partA(data, possibilities) {
  return new Promise((resolve) => {
    let path = traverse(possibilities, [], 0);
    let oneJolt = 0;
    let threeJolt = 0;
    for (let i = 0; i < path.length - 1; i++) {
      let difference = path[i + 1] - path[i];
      if (difference == 1) {
        oneJolt++;
      } else if (difference == 3) {
        threeJolt++;
      }
    }

    resolve(oneJolt * threeJolt);
  });
}

function getPossibleConnections(data, value) {
  let possibilities = [];
  data.forEach((element) => {
    let difference = element - value;
    if (difference > 0 && difference < 4) {
      possibilities.push(element);
    }
  });
  return possibilities;
}

function traverse(possibilities, path, value) {
  path.push(value);
  if (path.length == Object.keys(possibilities).length) {
    return path;
  }

  for (let i = 0; i < possibilities[value].length; i++) {
    if (!path.includes(possibilities[value][i])) {
      curr = traverse(possibilities, path.slice(), possibilities[value][i]);
      if (curr.length == Object.keys(possibilities).length) {
        return curr;
      }
    }
  }

  return path;
}

async function partB(data, possibilities) {
  return new Promise((resolve) => {
    let builtIn = Math.max(...data);
    let pathCount = {};
    data
      .slice()
      .reverse()
      .forEach((element) => {
        pathCount = countPaths(possibilities, builtIn, element, pathCount);
      });
    resolve(pathCount[0]);
  });
}

function countPaths(possibilities, builtIn, value, pathCount) {
  if (builtIn == value) {
    pathCount[value] = 1;
    return pathCount;
  }

  let count = 0;
  possibilities[value].forEach((element) => {
    if (element in pathCount) {
      count += pathCount[element];
    } else {
      count += countPaths(possibilities, builtIn, element, pathCount);
    }
  });

  pathCount[value] = count;
  return pathCount;
}

async function main() {
  try {
    var data = readFile('\n', parseInt);
    data.push(0);
    data.push(Math.max(...data) + 3);
    data.sort((a, b) => a - b);

    var possibilities = {};
    data.forEach((element) => {
      possibilities[element] = getPossibleConnections(data, element);
    });
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let answers = await Promise.all([
    partA(data, possibilities),
    partB(data, possibilities),
  ])
    .then((answers) => {
      console.log(`Part A: ${answers[0]}`);
      console.log(`Part B: ${answers[1]}`);
    })
    .catch(console.log);
}

main();
