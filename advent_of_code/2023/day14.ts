import { readInput } from './utils';

const data = readInput(data => data.split('\n').map(line => line.split(''))) as string[][];

const move = (vertical: boolean = true, end = false) => {
  const rows = data.length;
  const cols = data[0].length;

  for (let i = 0; i < (vertical ? cols : rows); i++) {
    let count = 0;
    let start = 0;
    for (let j = 0; j < (vertical ? rows : cols); j++) {
      if (vertical) {
        if (data[j][i] === 'O') {
          count++;
        }
        if (data[j][i] === '#' || j === cols - 1) {
          for (let k = start; k <= j; k++) {
            if (data[k][i] === '#') {
              continue;
            }
            if (end) {
              data[k][i] = k < j - count + (data[j][i] === '#' ? 0 : 1) ? '.' : 'O';
            } else {
              data[k][i] = k < start + count ? 'O' : '.';
            }
          }
          start = j + 1;
          count = 0;
        }
      } else {
        if (data[i][j] === 'O') {
          count++;
        }
        if (data[i][j] === '#' || j === rows - 1) {
          for (let k = start; k <= j; k++) {
            if (data[i][k] === '#') {
              continue;
            }
            if (end) {
              data[i][k] = k < j - count + (data[i][j] === '#' ? 0 : 1) ? '.' : 'O';
            } else {
              data[i][k] = k < start + count ? 'O' : '.';
            }
          }
          start = j + 1;
          count = 0;
        }
      }
    }
  }
}

const partA = () => {
  move(true, false);
  return data.reduce((acc, line, i) => {
    line.forEach((value) => {
      if (value === 'O') {
        acc += data.length - i;
      }
    });
    return acc;
  }, 0);
};

const partB = () => {
  let cache: Record<string, number[]> = {};
  let count = 0;

  while (count < 1000000000) {
    move(true, false);
    move(false, false);
    move(true, true);
    move(false, true);

    const curr = data.flat().join('');
    if (!(curr in cache)) {
      cache[curr] = [count];
    } else {
      cache[curr].push(count);
    }

    if (cache[curr].length === 3 && cache[curr][2] - cache[curr][1] === cache[curr][1] - cache[curr][0]) {
      const diff = cache[curr][1] - cache[curr][0];
      const remaining = 1000000000 - count;
      const div = Math.floor(remaining / diff);
      count += div * diff;
    }

    count++;
  }

  return data.reduce((acc, line, i) => {
    line.forEach((value) => {
      if (value === 'O') {
        acc += data.length - i;
      }
    });
    return acc;
  }, 0);
};

console.log('Part A:', partA());
console.log('Part B:', partB());
