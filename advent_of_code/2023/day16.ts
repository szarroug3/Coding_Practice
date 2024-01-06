import { readInput } from './utils';

const data = readInput((data) => data.split('\n').map(line => line.split(''))) as string[][];
type BeamType = { x: number, y: number, direction: { x: number, y: number } };

const directions = {
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 },
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 }
};

const getDirection = (beam: BeamType) => {
  if (beam.direction.x === 1) {
    return 'right';
  }
  if (beam.direction.x === -1) {
    return 'left';
  }
  if (beam.direction.y === 1) {
    return 'down';
  }
  return 'up';
}

const move = (beams: Array<BeamType>, energized: Record<number, Record<number, string[]>>) => {
  let added = false;
  for (let i = beams.length - 1; i >= 0; i--) {
    const direction = getDirection(beams[i]);
    if (!(beams[i].y in energized)) {
      energized[beams[i].y] = { [beams[i].x]: [direction] };
      added = true;
    } else if (!(beams[i].x in energized[beams[i].y])) {
      energized[beams[i].y][beams[i].x] = [direction];
      added = true;
    } else if (!energized[beams[i].y][beams[i].x].includes(direction)) {
      energized[beams[i].y][beams[i].x].push(direction);
      added = true;
    } else {
      beams.splice(i, 1);
      continue;
    }

    switch (data[beams[i].y][beams[i].x]) {
      case '/':
        switch (direction) {
          case 'left':
            beams[i].direction = directions.down;
            break;
          case 'right':
            beams[i].direction = directions.up;
            break;
          case 'up':
            beams[i].direction = directions.right;
            break;
          default:
            beams[i].direction = directions.left;
            break;
        }
        break;
      case '\\':
        switch (direction) {
          case 'left':
            beams[i].direction = directions.up;
            break;
          case 'right':
            beams[i].direction = directions.down;
            break;
          case 'up':
            beams[i].direction = directions.left;
            break;
          default:
            beams[i].direction = directions.right;
            break;
        }
        break;
      case '|':
        switch (direction) {
          case 'left':
          case 'right':
            beams[i].direction = directions.up;
            beams.push({ x: beams[i].x, y: beams[i].y, direction: directions.down });
            break;
          default:
            break;
        }
        break;
      case '-':
        switch (direction) {
          case 'up':
          case 'down':
            beams[i].direction = directions.left;
            beams.push({ x: beams[i].x, y: beams[i].y, direction: directions.right });
            break;
          default:
            break;
        }
        break;
      default:
        break;
    }

    beams[i].x += beams[i].direction.x;
    beams[i].y += beams[i].direction.y;
  }

  return { beams, energized, added };
};

const calculate = (beam: BeamType) => {
  let beams = [beam];
  let energized: Record<number, Record<number, string[]>> = {
    '-1': {},
    [data.length]: {},
  };

  for (let i = -1; i <= data[0].length; i++) {
    energized[-1][i] = ['down', 'right', 'left', 'up'];
    energized[data.length][i] = ['down', 'right', 'left', 'up'];
  }

  for (let i = 0; i < data.length; i++) {
    energized[i] = {
      '-1': ['down', 'right', 'left', 'up'],
      [data[i].length]: ['down', 'right', 'left', 'up']
    };
  }

  while (true) {
    let added;
    ({ beams, energized, added } = move(beams, energized));

    if (!added) {
      break;
    }
  }

  return Object.values(energized).reduce((acc, values) => {
    return acc + Object.keys(values).length;
  }, 0 - ((data.length) * 2) - (data[0].length * 2) - 4);
}

const partA = () => {
  return calculate({ x: 0, y: 0, direction: { x: 1, y: 0 } });
};

const partB = () => {
  const options = [];
  for (let i = 0; i < data[0].length; i++) {
    options.push({ x: i, y: 0, direction: directions.down });
    options.push({ x: i, y: data.length, direction: directions.up });
  }

  for (let i = 0; i < data.length; i++) {
    options.push({ x: 0, y: i, direction: directions.right });
    options.push({ x: data.length - 1, y: i, direction: directions.left });
  }

  return options.reduce((acc, option) => Math.max(acc, calculate(option)), 0);
};

console.log('Part A:', partA());
console.log('Part B:', partB());
