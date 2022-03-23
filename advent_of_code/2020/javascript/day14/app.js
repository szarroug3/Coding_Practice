// https://adventofcode.com/2020/day/#

const { readFile } = require('../utils/input');

function parse(data) {
  const re = /mem\[(\d+)\] = (\d+)/;
  let instructions = [];
  data.forEach((instruction) => {
    if (instruction.includes('mask')) {
      let mask = {};
      let maskData = data[0].split(' = ')[1];
      for (let i = 0; i < maskData.length; i++) {
        if (maskData[i] != 'X') {
          mask[i] = maskData[i];
        }
      }
      instructions.push([mask]);
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
    let mask = ''.padStart(36, '0');
    instructions.forEach((instruction) => {
      if (instruction.length == 1) {
        mask = instruction[0];
      } else {
        let address = instruction[0];
        let value = maskValue(mask, instruction[1]);
        memory[address] = value;
      }
    });

    let sum = BigInt(0);
    console.log(memory);
    for (let value of Object.values(memory)) {
      sum += BigInt(parseInt('0' + value, 2));
    }

    resolve(sum);
  });
}

function maskValue(mask, data) {
  data = data.toString(2).padStart(36, '0').split('');
  for (const [i, value] of Object.entries(mask)) {
    data[i] = value;
  }
  return data.join('');
}

async function partB(data) {
  return new Promise((resolve) => {
    resolve('UPDATE THIS');
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
