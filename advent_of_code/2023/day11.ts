import { readInput } from './utils';

const map = readInput((data) => {
  const lines = data.split('\n');
  return lines.map((line) => line.split(''));
}) as string[][];

const age = (map: string[][], years: number) => {
  let rowOffset = 0;
  let emptyCols = map[0].reduce((acc, value, i) => value === '.' ? [...acc, i] : acc, [] as number[]);

  const data: number[][] = [];
  map.forEach((line, row) => {
    line.forEach((value, col) => {
      if (value === '#') {
        data.push([row + rowOffset, col]);
        emptyCols = emptyCols.filter((c) => c !== col)
      }
    });

    if (!line.includes('#')) {
      rowOffset += years;
    }
  });

  const colOffsets: number[] = [];
  let offset = 0;
  for (let i = 0; i < map[0].length; i++) {
    if (emptyCols.includes(i)) {
      offset += years;
    }
    colOffsets.push(offset);
  }

  return data.map(([row, col]) => [row, col + colOffsets[col]]);
};

const partA = () => {
  const aged = age(map, 1);
  let total = 0;
  for (let i = 0; i < aged.length; i++) {
    const [row, col] = aged[i];
    for (let j = i+1; j < aged.length; j++) {
      const [currRow, currCol] = aged[j];
      total += Math.abs(row - currRow) + Math.abs(col - currCol);
    }
  }
  return total;
};

const partB = () => {
  const aged = age(map, 999999);
  let total = 0;
  for (let i = 0; i < aged.length; i++) {
    const [row, col] = aged[i];
    for (let j = i+1; j < aged.length; j++) {
      const [currRow, currCol] = aged[j];
      total += Math.abs(row - currRow) + Math.abs(col - currCol);
    }
  }
  return total;
};

console.log('Part A:', partA());
console.log('Part B:', partB());