import { readInput } from './utils.js';

const partA = () => {
  const re = /[0-9]/g;

  return data.reduce((total, line) => {
    const matches = line.match(re);
    if (!matches) {
      return total;
    }

    return total + Number(`${matches[0]}${matches[matches.length - 1]}`);
  }, 0);
}

const partB = () => {
  const words = "one|two|three|four|five|six|seven|eight|nine"
  const firstRe = new RegExp(`[0-9]|${words}`, 'g')
  const lastRe = new RegExp(`.*([0-9]|${words}).*$`, 'g')

  const convert = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4, 
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8, 
    'nine': 9,
  }

  return data.reduce((total, line) => {
    const first = line.match(firstRe);
    const last = lastRe.exec(line);
    lastRe.lastIndex = 0;

    if (!first | !last) {
      return total;
    }

    const firstNum = convert[first[0]] ?? first[0];
    const lastNum = convert[last[1]] ?? last[1];

    return total + Number(`${firstNum}${lastNum}`);
  }, 0);
};

const data = readInput((data) => data.split('\n'));
console.log('Part A: ', partA());
console.log('Part B: ', partB());
