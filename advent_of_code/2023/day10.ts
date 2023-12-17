import { readInput } from "./utils";

const checks: Record<string, Record<string, string[]>> = {
  '|': {
    up: ['|', '7', 'F', 'S'],
    down: ['|', 'J', 'L', 'S'],
  },
  '-': {
    left: ['-', 'L', 'F', 'S'],
    right: ['-', 'J', '7', 'S'],
  },
  'L': {
    up: ['|', '7', 'F', 'S'],
    right: ['-', 'J', '7', 'S'],
  },
  'J': {
    up: ['|', '7', 'F', 'S'],
    left: ['-', 'L', 'F', 'S'],
  },
  '7': {
    down: ['|', 'J', 'L', 'S'],
    left: ['-', 'L', 'F', 'S'],
  },
  'F': {
    right: ['-', 'J', '7', 'S'],
    down: ['|', 'J', 'L', 'S'],
  },
  'S': {
    up: ['|', '7', 'F'],
    right: ['-', 'J', '7'],
    down: ['|', 'J', 'L'],
    left: ['-', 'L', 'F'],
  },
};

const offsets: Record<string, number[]> = {
  up: [-1, 0],
  right: [0, 1],
  down: [1, 0],
  left: [0, -1],
}


const countSurroundingPipes = (map: string[][], row: number, col: number) => {
  const pipe = map[row][col];
  let pipes = [];
  for (let direction of Object.keys(checks[pipe])) {
    const currRow = row + Number(offsets[direction][0]);
    const currCol = col + Number(offsets[direction][1]);
    if (currRow >= 0 && currRow < map.length && currCol >= 0 && currCol < map[currRow].length) {
      pipes.push([currRow, currCol]);
    }
  }
  return pipes;
};

const cleanUpMap = (map: string[][], row: number, col: number) => {
  const queue = [[row, col]];
  const starting = new Set<number>();
  starting.add(col);
  const pipes: Record<number, Set<number>> = { [row]: starting };
  const visited: Record<number, Set<number>> = { [row]: starting };

  while (queue.length) {
    const [row, col] = queue.shift()!;
    if (!(row in pipes)) {
      pipes[row] = new Set();
    }
    const confirmed = countSurroundingPipes(map, row, col);
    if (confirmed.length < 2) {
      if (col in pipes[row]) {
        pipes[row].delete(col);
      }
      map[row][col] = '.';
      if (col - 1 in pipes[row]) {
        queue.push([row, col - 1]);
      }
      if (row in pipes && col + 1 in pipes[row]) {
        queue.push([row, col + 1]);
      }
      if (row - 1 in pipes && col in pipes[row - 1]) {
        queue.push([row - 1, col]);
      }
      if (row + 1 in pipes && col in pipes[row + 1]) {
        queue.push([row + 1, col]);
      }
    } else {
      pipes[row].add(col);
      confirmed.forEach(([row, col]) => {
        if (!(row in visited) || !visited[row].has(col)) {
          if (!(row in visited)) {
            visited[row] = new Set();
          }
          visited[row].add(col);
          queue.push([row, col]);
        }
      });
    }
  }

  for (let i = 0; i < map.length; i++) {
    for (let j = 0; j < map[i].length; j++) {
      if (!(i in pipes) || !pipes[i].has(j)) {
        map[i][j] = '.';
      }
    }
  }

  return { map, pipes };
};

const { map, pipes, startingRow, startingCol } = readInput((data) => {
  const map = data.split('\n').map((line) => line.split(''));

  const row = map.findIndex((line) => line.includes('S'));
  const col = map[row].findIndex((char) => char === 'S');

  return { ...cleanUpMap(map, row, col), startingRow: row, startingCol: col };
}) as { map: string[][], pipes: Record<number, Set<number>>, startingRow: number, startingCol: number };

const partA = () => {
  const count = Object.values(pipes).reduce((acc, row) => acc + row.size, 0);
  return Math.ceil(count / 2);
};

const orderBoundary = () => {
  const clockwise: number[][] = [[startingRow, startingCol]];
  const visited: Record<number, Set<number>> = {[startingRow]: new Set([startingCol])};
  let row = startingRow;
  let col = startingCol;

  while (true) {
    let symbol = map[row][col];
    for (let direction of Object.keys(checks[map[row][col]])) {
      const currRow = row + Number(offsets[direction][0]);
      const currCol = col + Number(offsets[direction][1]);
      if (currRow < 0 || currRow >= map.length || currCol < 0 || currCol >= map[currRow].length) {
        continue;
      }

      const currSymbol = map[currRow][currCol];
      if (!checks[symbol][direction].includes(currSymbol)) {
        continue;
      }

      if (currRow === startingRow && currCol === startingCol && clockwise.length > 2) {
        clockwise.push([currRow, currCol]);
        return clockwise;
      }

      if ((currRow in visited && visited[currRow].has(currCol)) ||
        (!(currRow in pipes) || !pipes[currRow].has(currCol))) {
        continue;
      }

      if (!(currRow in visited)) {
        visited[currRow] = new Set<number>();
      }
      visited[currRow].add(currCol);
      clockwise.push([currRow, currCol]);


      row = currRow;
      col = currCol;
      break;
    }
  }
};

const findArea = (boundary: number[][]) => {
  let area = 0;

  for (let i = 0; i < boundary.length - 1; i++) {
    const [x0, y0] = boundary[i];
    const [x1, y1] = boundary[i+1];
    area += (x0 * y1) - (x1 * y0);
  }

  return Math.abs(area / 2);
}

const partB = () => {
  const boundary: number[][] = orderBoundary();
  const area = findArea(boundary);

  return Math.ceil(area - (boundary.length / 2) + 1);
};

console.log('Part A', partA());
console.log('Part B', partB());