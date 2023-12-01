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

const reverse = (str) => {
  return str.split('').reverse().join('');
};

const partB = () => {
  const words = "one|two|three|four|five|six|seven|eight|nine"
  const backwords = reverse(words);

  const re = new RegExp(`[0-9]|${words}`, 'g')
  const backwordsRe = new RegExp(`[0-9]|${backwords}`, 'g')

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
    const matches = line.match(re);
    const backwardsMatches = reverse(line).match(backwordsRe);
    if (!matches | !backwardsMatches) {
      return total;
    }

    const first = convert[matches[0]] ?? matches[0];
    let last = backwardsMatches[0].split('').reverse().join('');
    last = convert[last] ?? last;

    return total + Number(`${first}${last}`);
  }, 0);
};

const data = readInput((data) => data.split('\n'));
console.log('Part A: ', partA());
console.log('Part B: ', partB());
