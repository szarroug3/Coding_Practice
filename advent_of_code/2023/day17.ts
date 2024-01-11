import { readInput } from './utils';

const data = readInput((data) => data.split('\n').map(line => line.split('').map(Number))) as number[][];

const addState = (y: number, x: number, dy: number, dx: number, cost: number, states: Record<number, string[]>, visited: Record<number, Record<number, Record<number, Record<number, number[]>>>>, min: number, max: number) => {
  const directions = [
    [dx, -dy],
    [-dx, dy],
  ]

  for (let [dy, dx] of directions) {
    if (!(y in visited)) {
      visited[y] = {};
    }
    if (!(x in visited[y])) {
      visited[y][x] = {};
    }
    if (!(dy in visited[y][x])) {
      visited[y][x][dy] = {};
    }
    if (!(dx in visited[y][x][dy])) {
      visited[y][x][dy][dx] = [];
    }
    visited[y][x][dy][dx].push(0);

    const minY = y + dy * min;
    const minX = x + dx * min;

    if (minY < 0 || minX < 0 || minY >= data.length || minX >= data[0].length) {
      continue;
    }

    let currX = x;
    let currY = y;
    let currCost = cost;

    for (let i = 0; i < max; i++) {
      currX += dx;
      currY += dy;

      if (currX < 0 || currY < 0 || currX >= data[0].length || currY >= data.length) {
        break;
      }

      if (currY in visited && currX in visited[currY] && dy in visited[currY][currX] && dx in visited[currY][currX][dy] && visited[currY][currX][dy][dx].includes(i + 1)) {
        continue;
      }

      currCost += data[currY][currX];

      if (!(currY in visited)) {
        visited[currY] = {};
      }
      if (!(currX in visited[currY])) {
        visited[currY][currX] = {};
      }
      if (!(dy in visited[currY][currX])) {
        visited[currY][currX][dy] = {};
      }
      if (!(dx in visited[currY][currX][dy])) {
        visited[currY][currX][dy][dx] = [];
      }
      visited[currY][currX][dy][dx].push(i + 1);

      if (i >= min - 1) {
        if (!(currCost in states)) {
          states[currCost] = [];
        }
        states[currCost].push([currY, currX, dy, dx].join(','));
      }
      if (y === data.length - 1 && x === data[0].length - 1) {
        return { states, visited };
      }
    }
  }

  return { found: -1, states, visited };
};

const getAndRemoveLowestCostState = (states: Record<number, string[]>) => {
  const min = Number(Object.entries(states)[0][0]);
  states[min].sort((a, b) => {
    const [ay, ax] = a.split(',').map(Number);
    const [by, bx] = b.split(',').map(Number);
    return  (bx + by) - (ax + ay);
  });

  let state = states[min][0].split(',').map(Number);
  states[min].splice(0, 1);
  if (!states[min].length) {
    delete states[min];
  }
  return { cost: min, state, states };
};

const djikstra = (min: number, max: number) => {
  let visited: Record<number, Record<number, Record<number, Record<number, number[]>>>> = {}; // y, x, dy, dx
  let states: Record<number, string[]> = {0: ['0,0,-1,0', '0,0,0,-1,0']}; // y, x, dy, dx, cost
  let x = 0;
  let y = 0;
  let dx = 1;
  let dy = 0;
  let cost = 0;
  let found;

  while (true) {
    ({ cost, state: [y, x, dy, dx], states } = getAndRemoveLowestCostState(states));
    if (y === data.length - 1 && x === data[0].length - 1) {
      return cost;
    }

    ({ found, states, visited } = addState(y, x, dy, dx, cost, states, visited, min, max));
    if (found !== -1) {
      return found;
    }
  }
}

const partA = () => {
  return djikstra(1, 3);
};

const partB = () => {
  return djikstra(4, 10);
};

console.log('Part A: ', partA());
console.log('Part B: ', partB());
