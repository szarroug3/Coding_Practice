import { readInput } from './utils';

const data = readInput((data) => {
  return data.split('\n').map((line) => {
    const [springs, order] = line.split(' ');
    const values = order.split(',').map(Number);
    return { springs, values };
  });
}) as Array<{ springs: string, values: number[] }>;

const simplifyEnds = (split: string[], values: number[]) => {
  if (split.length < 1) {
    return { split, values };
  }

  while (split.length && (split[0].startsWith('#') || split[0].startsWith('?#') || split[0].length < values[0])) {
    if (split[0].startsWith('#')) {
      if (split[0].length <= values[0] + 1) {
        split.shift();
      } else {
        split[0] = split[0].slice(values[0] + 1);
      }
      values.shift();
    } else if (split[0].length < values[0]) {
      split.shift();
    } else if (!split[0].slice(1, values[0] + 1).includes('?')) {
      split[0] = split[0].slice(values[0] + 2);
      values.shift();
    } else {
      break;
    }
  }

  while (split.length && (split[split.length - 1].endsWith('#') || split[split.length - 1].endsWith('#?') || split[split.length - 1].length < values[values.length - 1])) {
    const last = split[split.length - 1];
    if (last.endsWith('#')) {
      if (last.length <= values[values.length - 1] + 1) {
        split.pop();
      } else {
        split[split.length - 1] = last.slice(0, -values[values.length - 1] - 1);
      }
      values.pop();
    } else if (last.length < values[values.length - 1]) {
      split.pop();
    } else if (!last.slice(-values[values.length - 1] - 1, -1).includes('?')) {
      split[split.length - 1] = last.slice(0, -values[values.length - 1] - 2);
      values.pop();
    } else {
      break;
    }
  }

  return { split, values };
};

const expandKnown = (split: string[], values: number[]) => {
  if (split.length < 1) {
    return { split, values };
  }

  const possible: Record<number, { splitIndex: number, ignore: boolean, minEnd: number, maxStart: number }> = {};

  let valueIndex = 0;
  for (let splitIndex = 0; splitIndex < split.length && valueIndex < values.length; splitIndex++) {
    let length = -1;

    while (valueIndex < values.length && length + values[valueIndex] + 1 <= split[splitIndex].length) {
      while (split[splitIndex][length + values[valueIndex] + 1] === '#') {
        length++;
      }

      length += values[valueIndex] + 1;
      possible[valueIndex] = { splitIndex, ignore: false, minEnd: length, maxStart: -1 };
      valueIndex++;
    }
  }

  valueIndex = values.length - 1;
  for (let splitIndex = split.length - 1; splitIndex >= 0 && valueIndex >= 0; splitIndex--) {
    let length = -1;

    const curr = split[splitIndex];

    while (valueIndex >= 0 && length + values[valueIndex] + 1 <= split[splitIndex].length) {
      while (curr[curr.length - length - values[valueIndex] - 2] === '#') {
        length++;
      }

      length += values[valueIndex] + 1;
      if (possible[valueIndex].splitIndex !== splitIndex) {
        possible[valueIndex].ignore = true;
      } else {
        possible[valueIndex].maxStart = curr.length - length;
      }

      valueIndex--;
    }
  }

  Object.values(possible).filter(({ ignore, minEnd, maxStart }) => !ignore && maxStart < minEnd).forEach(({ splitIndex, maxStart, minEnd }) => {
    split[splitIndex] = split[splitIndex].slice(0, maxStart).padEnd(minEnd, '#') + split[splitIndex].slice(minEnd);
  });

  return { split, values };
};

const simplifySingleValue = (split: string[], values: number[]) => {
  if (values.length !== 1 || !split.join('.').includes('#')) {
    return split;
  }

  split = split.filter((value) => value.includes('#'));

  const first = Math.min(split[0].indexOf('#'), split[0].length - values[0]);
  const last = Math.max(split[0].lastIndexOf('#'), values[0] - 1);
  const length = last - first + 1;
  const remaining = values[0] - last + first - 1;
  split[0] = ''.padEnd(remaining, '?') + ''.padEnd(length, '#') + ''.padEnd(remaining, '?');

  return split;
};

const simplify = (springs: string, values: number[]) => {
  let split = springs.split('.').filter((value) => value.length);
  springs = split.join('.')
  values = [...values];
  let last = '';

  while (last !== springs && springs.length > 0) {
    last = springs;
    ({ split, values } = simplifyEnds(split, values));
    ({ split, values } = expandKnown(split, values));
    split = simplifySingleValue(split, values);
    springs = split.join('.');
  }

  return { springs, values };
};

const updateCache = (springs: string, values: string, cache: Record<string, Record<string, number>>) => {
  const maxValue = Math.max(...values.split('.').map(Number));

  let used = '';
  while (springs.length) {
    let piece = springs;
    while (!(piece in cache)) {
      if (!piece.includes('?')) {
        cache[piece] = { [piece.length]: 1 };
      } else if (!piece.includes('#')) {
        cache[piece] = {};
        const max = parseInt(''.padEnd(piece.length, '1'), 2);
        for (let i = 0; i <= max; i++) {
          let curr = i.toString(2).padStart(piece.length, '0');
          let filtered = curr.split('0').filter((value) => value.length).map((value) => value.length) || [];
          if (filtered.some((value) => value > maxValue)) {
            continue;
          }

          if (curr.startsWith('0') && filtered[0] !== 0) {
            filtered.unshift(0);
          }
          if (curr.endsWith('0') && filtered[filtered.length - 1] !== 0) {
            filtered.push(0);
          }

          const joined = filtered.join('.');
          cache[piece][joined] = (cache[piece][joined] || 0) + 1;
        }
      } else {
        piece = piece.slice(0, -1);
      }
    }

    springs = springs.slice(piece.length);

    const combined = used + piece;
    if (!(combined in cache)) {
      cache[combined] = {};
      const considerations = Object.entries(cache[used])
        .filter(([possible]) => values.includes(possible.split('.').slice(1, -1).filter((value) => value !== '0').join('.')));
      for (let [possible, amount] of considerations) {
        let split = !possible.length ? [] : possible.split('.').map((value) => Number(value));

        for (let [currPiece, count] of Object.entries(cache[piece])) {
          let splitPiece = !currPiece.length ? [] : currPiece.split('.').map((value) => Number(value));
          let result;

          if (split.length && splitPiece.length) {
            if (split[split.length - 1] && splitPiece[0]) {
              result = split.slice(0, -1);
              result.push(split[split.length - 1] + splitPiece[0]);
              result.push(...splitPiece.slice(1));
            } else {
              result = [...split, ...splitPiece];
            }
          } else if (split.length) {
            result = [...split];
          } else {
            result = [...splitPiece];
          }

          if (result.some((value) => value > maxValue)) {
            continue;
          }

          if (!values.includes(result.slice(1, -1).filter((value) => value > 0).join('.'))) {
            continue;
          }

          const joined = result.filter((value, index) => index === 0 || index === result.length - 1 || value > 0).join('.');

          if (!(joined in cache[combined])) {
            cache[combined][joined] = amount * count;
          } else {
            cache[combined][joined] += (amount * count);
          }
        }
      }
    }

    used = combined;
  }

  return cache;
};

const getPossibleValues = (springs: string, values: number[]) => {
  const joined = values.join('.');
  const split = springs.split('.').filter((value) => value.length);
  let possibilities: Record<string, number> = {};
  let cache: Record<string, Record<string, number>> = { '': { '': 1 } };

  for (let i = 0; i < split.length; i++) {
    if (!(split[i] in cache)) {
      cache = updateCache(split[i], joined, cache);
    }

    if (!Object.keys(possibilities).length) {
      possibilities = cache[split[i]];
    } else {
      possibilities = Object.entries(possibilities).reduce((acc, [possibility, count]) => {
        if (!joined.startsWith(possibility.split('.').filter((value) => value && value !== '0').join('.'))) {
          return acc;
        }
        for (let [value, currCount] of Object.entries(cache[split[i]])) {
          const curr = [possibility, value].join('.').split('.').filter((value) => value && value !== '0').join('.');
          if (joined.startsWith(curr)) {
            acc[curr] = (acc[curr] || 0) + (count * currCount);
          }
        }
        return acc;
      }, {} as Record<string, number>);
    }
  }

  return Object.entries(possibilities).filter(([possibility]) => possibility.split('.').filter((value) => value !== '0').join('.') === joined).reduce((acc, [_, value]) => acc + value, 0);
};

const calculate = (springs: string, values: number[]) => {
  if (!springs.includes('#') && !springs.includes('.')) {
    return calculateUnknownOnly(springs, values);
  }

  let possible = springs.replace('.', '').length;
  let known = springs.split('#').length - 1;
  let needed = values.reduce((acc, value) => acc + value, 0);
  if (possible === needed || known == needed) {
    return 1;
  }

  const { springs: simplifiedSprings, values: simplifiedValues } = simplify(springs, values);
  possible = simplifiedSprings.replace('.', '').length;
  needed = simplifiedValues.reduce((acc, value) => acc + value, 0);
  known = simplifiedSprings.split('#').length - 1;

  if (possible === needed || known == needed) {
    return 1;
  } else if (!simplifiedValues.length) {
    return 1;
  } else if (simplifiedValues.length === 1) {
    return simplifiedSprings.split('.').filter((spring) => spring.length >= simplifiedValues[0]).reduce((acc, spring) => acc + spring.length - simplifiedValues[0] + 1, 0);
  }
  return getPossibleValues(simplifiedSprings, simplifiedValues);
};

const partA = () => {
  return data.reduce((acc, { springs, values }) => acc + calculate(springs, values), 0);
};

const factorial = (number: number) => {
  let result = 1;
  for (let i = 2; i <= number; i++) {
    result *= i;
  }
  return result;
};

const calculateUnknownOnly = (springs: string, values: number[]) => {
  const needed = values.reduce((acc, value) => acc + value, values.length - 1);
  const extra = springs.length - needed;
  const spaces = values.length + 1;
  return factorial(extra + spaces - 1) / (factorial(spaces - 1) * factorial(extra));
}

const partB = () => {
  return data.reduce((acc, { springs, values }) => {
    springs = `${springs}?${springs}?${springs}?${springs}?${springs}`;
    values = [...values, ...values, ...values, ...values, ...values];
    return acc + calculate(springs, values);
  }, 0);
};

console.log('Part A:', partA());
console.log('Part B:', partB());
