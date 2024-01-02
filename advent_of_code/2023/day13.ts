import { readInput } from "./utils";

const data = readInput((data) => {
  return data.split('\n\n').reduce((acc, pattern) => {
    acc.push(pattern.split('\n').map((line) => line.split('')));
    return acc;
  }, [] as string[][][])
}) as string[][][];

const getMatches = (line: string[]) => {
  const matches: number[] = [];
  for (let i = 1; i < line.length; i++) {
    const distance = Math.min(i, line.length - i);
    const left = line.slice(i - distance, i).join('');
    const right = line.slice(i, i + distance).reverse().join('');

    if (left === right) {
      matches.push(i);
    }
  }
  return matches;
}

const check = (pattern: string[][], ignore: Record<number, boolean> = {}) => {
  let matches = getMatches(pattern[0]);
  for (let i = 1; i < pattern.length; i++) {
    matches = matches.filter(value => getMatches(pattern[i]).includes(value));
  }

  let found = matches.find(value => !(value in ignore) || !ignore[value]);
  if (found) {
    return { value: found, vertical: true };
  }

  const flipped: string[][] = [];
  for (let i = 0; i < pattern[0].length; i++) {
    const row: string[] = [];
    for (let j = 0; j < pattern.length; j++) {
      row.push(pattern[j][i]);
    }
    flipped.push(row);
  }

  matches = getMatches(flipped[0]);
  for (let i = 1; i < flipped.length; i++) {
    matches = matches.filter(value => getMatches(flipped[i]).includes(value));
  }

  found = matches.find(value => !(value * 100 in ignore) || ignore[value]);
  if (found) {
    return { value: found * 100, vertical: false };
  }

  return { value: -1, vertical: false };
}

const partA = () => {
  return data.reduce((acc, pattern) => {
    acc += check(pattern).value;
    return acc;
  }, 0);
};

const partB = () => {
  return data.reduce((acc, pattern) => {
    const original = check(pattern);
    const ignore = {[original.value]: original.vertical};
    for (let i = 0; i < pattern.length; i++) {
      for (let j = 0; j < pattern[i].length; j++) {
        pattern[i][j] = pattern[i][j] === '#' ? '.' : '#';
        const curr = check(pattern, ignore).value;
        if (curr !== -1) {
          return acc + curr;
        }
        pattern[i][j] = pattern[i][j] === '#' ? '.' : '#';
      }
    }
    return acc;
  }, 0);
};

console.log('Part A:', partA());
console.log('Part B:', partB());
