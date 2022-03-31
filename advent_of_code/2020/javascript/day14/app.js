// https://adventofcode.com/2020/day/14

const { readFile } = require('../utils/input');

function parse(data) {
  const re = /mem\[(\d+)\] = (\d+)/;
  let instructions = [];
  data.forEach((instruction) => {
    if (instruction.includes('mask')) {
      let mask = {};
      let maskData = instruction.split(' = ')[1];
      for (let i = 0; i < maskData.length; i++) {
        mask[i] = maskData[i];
      }
      instructions.push(mask);
    } else {
      let match = instruction.match(re);
      let address = parseInt(match[1]);
      let value = parseInt(match[2]);
      instructions.push([address, value]);
    }
  });
  return instructions;
}

async function partA(instructions) {
  return new Promise((resolve) => {
    let memory = {};
    let mask = {};
    instructions.forEach((instruction) => {
      if (instruction instanceof Array) {
        let address = instruction[0];
        memory[address] = maskValue(mask, instruction[1]);
      } else {
        mask = instruction;
      }
    });

    let sum = BigInt(0);
    for (let value of Object.values(memory)) {
      sum += BigInt(parseInt('0' + value, 2));
    }

    resolve(sum);
  });
}

function maskValue(mask, data) {
  data = data.toString(2).padStart(36, '0').split('');
  for (const [i, value] of Object.entries(mask)) {
    if (value !== 'X') {
      data[i] = value;
    }
  }
  return data.join('');
}

async function partB(instructions) {
  return new Promise((resolve) => {
    let memory = {};
    let mask = {};
    instructions.forEach((instruction) => {
      if (instruction instanceof Array) {
        let addresses = maskValueUsingFloating(mask, instruction[0]);
        addresses.forEach((address) => {
          memory[address] = instruction[1];
        });
      } else {
        mask = instruction;
      }
    });

    let sum = BigInt(0);
    for (let value of Object.values(memory)) {
      sum += BigInt(parseInt('0' + value));
    }

    resolve(sum);
  });
}

function getCombinations(length) {
  let values = [];
  for (let i = 0; i < 2 ** length; i++) {
    values.push(i.toString(2).padStart(length, '0'));
  }
  return values;
}

function maskValueUsingFloating(mask, data) {
  data = data.toString(2).padStart(36, '0').split('');

  xCount = 0;
  Object.values(mask).forEach((element) => {
    if (element == 'X') {
      xCount++;
    }
  });

  let xCombinations = getCombinations(xCount);
  let values = [];
  xCombinations.forEach((combination) => {
    let combinationIndex = 0;
    let curr = [];
    for (const [i, value] of Object.entries(mask)) {
      if (value === '1') {
        curr.push(value);
      } else if (value === 'X') {
        curr.push(combination[combinationIndex]);
        combinationIndex++;
      } else {
        curr.push(data[i]);
      }
    }
    values.push(curr.join(''));
  });

  return values;
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
