import { readInput } from './utils';

type MapType = Record<string, number[][]>;
const maps: MapType  = {};
const backwardsMaps: MapType  = {};

let seeds: Array<number>;

const mapNames = ['location', 'humidity', 'temperature', 'light', 'water', 'fertilizer', 'soil', 'seed'];

const sortMaps = (index: number) => {
  // sort maps by from value
  Object.keys(maps).forEach((key) => {
    maps[key].sort((a, b) => a[index] - b[index]);
  });
  Object.keys(backwardsMaps).forEach((key) => {
    backwardsMaps[key].sort((a, b) => a[index] - b[index]);
  });
};

const addMissingRanges = (index: number) => {
  mapNames.slice(0, mapNames.length - 1).forEach((key, mapIndex) => {
    const otherKey = mapNames[mapIndex + 1];
    maps[key].forEach((data, dataIndex) => {
      if (dataIndex === maps[key].length - 1) {
        maps[key].push([data[index] + data[2], data[index] + data[2], Infinity]);
        backwardsMaps[otherKey].push([data[index] + data[2], data[index] + data[2], Infinity]);
      }

      if (dataIndex === 0) {
        if (data[index] > 0) {
          maps[key].push([0, 0, data[index]]);
          backwardsMaps[otherKey].push([0, 0, data[index]]);
        }
        return;
      }

      const last = maps[key][dataIndex - 1];
      if (data[index] > last[index] && last[index] + last[2] + 1 < data[index]) {
        const newFrom = last[index] + last[2] + 1;
        const newRange = data[index] - newFrom;
        maps[key].push([newFrom, newFrom, newRange]);
        backwardsMaps[otherKey].push([newFrom, newFrom, newRange]);
      }
    });
  });
};

readInput((data) => {
  const lines = data.split('\n');
  seeds = [...lines[0].matchAll(/\d+/g)].map((match) => Number(match[0]));

  let toKey = '';
  let fromKey = '';

  lines.slice(1).forEach((line) => {
    if (line.includes('map')) {
      const keys = [...line.matchAll(/(.*)-to-(.*) map/g)];
      fromKey = keys[0][1];
      toKey = keys[0][2];
      maps[toKey] = [];
      backwardsMaps[fromKey] = [];
    } else if (line !== '') {
      const [fromValue, toValue, range] = [...line.matchAll(/(\d+) (\d+) (\d+)/g)][0].slice(1).map<number>(Number);

      maps[toKey].push([toValue, fromValue, range]);
      backwardsMaps[fromKey].push([fromValue, toValue, range]);
    }
  });

  // add missing from ranges
  sortMaps(0);
  addMissingRanges(0);

  // add missing to ranges
  sortMaps(1);
  addMissingRanges(1);

  sortMaps(0);
});

const getFromMap = (maps: MapType, key: string, value: number): number[] | null => {
  if (!(key in maps)) {
    return null;
  }

  return Object.values(maps[key]).find(([from, _, range]) => {
    return from <= value && value < from + range;
  })!;
};

const partA = () => {
  const getValue = (key: string, value: number): number => {
    const result = getFromMap(maps, key, value);
    if (!result) {
      return value;
    }

    const [from, to] = result;
    return value + (to - from);
  };

  return Math.min(...seeds.map((seed) => getValue('soil', seed))
    .map((soil) => getValue('fertilizer', soil))
    .map((fertilizer) => getValue('water', fertilizer))
    .map((water) => getValue('light', water))
    .map((light) => getValue('temperature', light))
    .map((temperature) => getValue('humidity', temperature))
    .map((humidity) => getValue('location', humidity))
  );
};

const partB = () => {
  const seedPairs: number[][] = [];
  for (let i = 0; i < seeds.length; i += 2) {
    seedPairs.push([seeds[i], seeds[i+1]])
  }
  seedPairs.sort((a, b) => a[0] - b[0]);

  const getRange = (key: string, value: number) => {
    return Object.values(backwardsMaps[key])
      .sort((a, b) => a[1] - b[1])
      .find(([, curr]) => {
        return curr > value + 1;
      })![1] - value - 1;
  };

  const getValue = (key: string, value: number, range: number): number[] => {
    const [from, to, conversionRange] = getFromMap(backwardsMaps, key, value)!;
    const remainingRange = from + conversionRange - value - 1;
    range = Math.min(remainingRange, range);

    return [value + (to - from), range];
  };

  let min = 0;
  let range = -1;
  let last: {
    min: number,
    next: number,
    state: Record<string, Record<string, number>>;
  } = {min, next: range, state: {}};

  let checkLast = false;

  while (true) {
    const offset = min - last.min;
    last.min = min;

    if (min <= last.next) {
      range = last.next - min;
    } else {
      range = getRange('humidity', min);
      last.next = range;
    }

    let value = min;

    mapNames.slice(1).forEach((key) => {
      if (checkLast && key in last.state && offset <= last.state[key].next - last.state[key].value) {
        range = last.state[key].next - last.state[key].value - offset;
        value = last.state[key].value + offset;
      } else {
        [value, range] = getValue(key, value, range);
        checkLast = false;
      }
      last.state[key] = {
        next: value + range,
        value
      };
    });

    const found = seedPairs.filter(([seed, seedRange]) => {
      return (seed <= value + range && value <= seed + seedRange);
    });

    if (found.length) {
      return min + Math.min(Math.max(found[0][0], value!), Math.max(found[0][0] + found[0][1], value! + range)) - value!;
    }

    min += range + 1;
    checkLast = true;
  }
};

console.log('Part A:', partA());
console.log('Part B:', partB());