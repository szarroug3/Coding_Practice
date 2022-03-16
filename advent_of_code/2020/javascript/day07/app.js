// https://adventofcode.com/2020/day/7

const { readFile } = require('../utils/input');

function parse(data) {
  let bags = {};
  const re = /(\d+) (\w+ \w+) bag/g;

  data.forEach((element) => {
    let values = element.split(' contain ');

    let bag = values[0].split(' ').slice(0, 2).join(' ');
    if (!(bag in bags)) {
      bags[bag] = [];
    }

    let matches = null;
    let results = [];
    while ((matches = re.exec(values[1]))) {
      results.push(matches.slice(1, 3));
    }

    results.forEach((match) => {
      if (!(match[1] in bags)) {
        bags[match[1]] = [];
      }
      bags[bag].push({
        count: parseInt(match[0]),
        name: match[1],
        type: bags[match[1]],
      });
    });
  });
  return bags;
}

function getHolders(data, name) {
  let holders = [];
  Object.keys(data).forEach((bagName) => {
    let found = data[bagName].find((bag) => {
      return bag.name == name;
    });

    if (found) {
      holders.push(bagName);
    }
  });

  return holders;
}

function getHoldersFromList(data, directHolders) {
  let holders = [];
  directHolders.forEach((bagName) => {
    let curr = getHolders(data, bagName);
    curr.forEach((currBag) => {
      if (!holders.includes(currBag)) {
        holders.push(currBag);
      }
    });
  });
  return holders;
}

function countBags(bags, bag) {
  let count = 0;
  bags[bag].forEach((subBag) => {
    count += subBag.count;
    count += subBag.count * countBags(bags, subBag.name);
  });
  return count;
}

async function partA(data) {
  return new Promise((resolve) => {
    let holders = getHolders(data, 'shiny gold');
    let currHolders = getHoldersFromList(data, holders);

    while (currHolders.length != 0) {
      currHolders.forEach((currBag) => {
        if (!holders.includes(currBag)) {
          holders.push(currBag);
        }
      });
      currHolders = getHoldersFromList(data, currHolders);
    }
    resolve(holders.length);
  });
}

async function partB(data) {
  return new Promise((resolve) => {
    resolve(countBags(data, 'shiny gold'));
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
