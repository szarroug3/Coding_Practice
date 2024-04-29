import { readInput } from "./utils";

type CoordinateType = {
  x: number;
  y: number;
  z: number;
}

type BrickType = {
  coordinates: CoordinateType[];
  id: number;
  axis: string;
}

const bricks = readInput(data => {
  return data.split('\n').map((line, id) => {
    const coordinates: CoordinateType[] = line.split('~').map((endpoint) => endpoint.split(',').map(Number)).map(endpoint => {
      return {
        x: endpoint[0],
        y: endpoint[1],
        z: endpoint[2]
      };
    });

    let axis;
    if (coordinates[0].x === coordinates[1].x) {
      axis = 'x';
    } else if (coordinates[0].y === coordinates[1].y) {
      axis = 'y';
    } else {
      axis = 'z';
    }

    return { coordinates, id, axis };
  });
}) as BrickType[];


const unsetMapForBrick = (map: Record<number, Record<number, Record<number, number>>>, { coordinates, id }: BrickType) => {
  const zMin = Math.min(coordinates[0].z, coordinates[1].z);
  const zMax = Math.max(coordinates[0].z, coordinates[1].z);

  const yMin = Math.min(coordinates[0].y, coordinates[1].y);
  const yMax = Math.max(coordinates[0].y, coordinates[1].y);

  const xMin = Math.min(coordinates[0].x, coordinates[1].x);
  const xMax = Math.max(coordinates[0].x, coordinates[1].x);

  for (let z = zMin; z <= zMax; z++) {
    for (let y = yMin; y <= yMax; y++) {
      for (let x = xMin; x <= xMax; x++) {
        delete map[z][y][x];
      }
    }
  }

  return map;
};

const setMapForBrick = (map: Record<number, Record<number, Record<number, number>>>, { coordinates, id }: BrickType) => {
  const zMin = Math.min(coordinates[0].z, coordinates[1].z);
  const zMax = Math.max(coordinates[0].z, coordinates[1].z);

  const yMin = Math.min(coordinates[0].y, coordinates[1].y);
  const yMax = Math.max(coordinates[0].y, coordinates[1].y);

  const xMin = Math.min(coordinates[0].x, coordinates[1].x);
  const xMax = Math.max(coordinates[0].x, coordinates[1].x);

  for (let z = zMin; z <= zMax; z++) {
    if (!(z in map)) {
      map[z] = {};
    }

    for (let y = yMin; y <= yMax; y++) {
      if (!(y in map[z])) {
        map[z][y] = {};
      }

      for (let x = xMin; x <= xMax; x++) {
        map[z][y][x] = id;
      }
    }
  }

  return map;
};

const generateMap = (bricks: BrickType[]) => {
  return bricks.reduce((map, brick) => setMapForBrick(map, brick), {} as Record<number, Record<number, Record<number, number>>>);
};

const canFallDistance = (map: Record<number, Record<number, Record<number, number>>>, coordinates: CoordinateType[]) => {
  let distance = 0;

  const zMin = Math.min(coordinates[0].z, coordinates[1].z);

  const yMin = Math.min(coordinates[0].y, coordinates[1].y);
  const yMax = Math.max(coordinates[0].y, coordinates[1].y);

  const xMin = Math.min(coordinates[0].x, coordinates[1].x);
  const xMax = Math.max(coordinates[0].x, coordinates[1].x);

  for (let z = zMin - 1; z > 0; z--) {
    for (let y = yMin; y <= yMax; y++) {
      for (let x = xMin; x <= xMax; x++) {
        if (z in map && y in map[z] && x in map[z][y]) {
          return distance;
        }
      }
    }
    distance++;
  }

  return distance;
};

const settle = (map: Record<number, Record<number, Record<number, number>>>, bricks: BrickType[]) => {
  let done = false;
  while (!done) {
    done = true;

    for (const brick of bricks) {
      const distance = canFallDistance(map, brick.coordinates);
      if (distance > 0) {
        map = unsetMapForBrick(map, brick);
        brick.coordinates[0].z -= distance;
        brick.coordinates[1].z -= distance;
        map = setMapForBrick(map, brick);
        done = false;
      }
    }
  }

  return { map, bricks };
}

const getDependencies = (map: Record<number, Record<number, Record<number, number>>>, bricks: BrickType[]) => {
  const dependencies: Record<number, number[]> = {};
  const supporting: Record<number, number[]> = {};
  for (const brick of bricks) {
    dependencies[brick.id] = [];
    supporting[brick.id] = [];

    const below = Math.min(brick.coordinates[0].z, brick.coordinates[1].z) - 1;
    const above = Math.max(brick.coordinates[0].z, brick.coordinates[1].z) + 1;

    const yMin = Math.min(brick.coordinates[0].y, brick.coordinates[1].y);
    const yMax = Math.max(brick.coordinates[0].y, brick.coordinates[1].y);

    const xMin = Math.min(brick.coordinates[0].x, brick.coordinates[1].x);
    const xMax = Math.max(brick.coordinates[0].x, brick.coordinates[1].x);

    if (above in map) {
      const row = map[above];

      for (let y = yMin; y <= yMax; y++) {
        if (!(y in row)) {
          continue;
        }
        for (let x = xMin; x <= xMax; x++) {
          if (!(x in row[y])) {
            continue;
          }
          if (!(map[above][y][x] in dependencies[brick.id])) {
            dependencies[brick.id].push(map[above][y][x]);
          }
        }
      }
    }

    if (below in map) {
      const row = map[below];

      for (let y = yMin; y <= yMax; y++) {
        if (!(y in row)) {
          continue;
        }
        for (let x = xMin; x <= xMax; x++) {
          if (!(x in row[y])) {
            continue;
          }
          if (!(map[below][y][x] in supporting[brick.id])) {
            supporting[brick.id].push(map[below][y][x]);
          }
        }
      }
    }
  }

  return { dependencies, supporting };
};

const wouldFall = (supporting: Record<number, number[]>, id: number, fell: number[]) => {
  return !supporting[id].some(sup => !fell.includes(sup));
};

const partA = () => {
  let current: BrickType[] = [...bricks];
  let map = generateMap(bricks);
  ({ map, bricks: current } = settle(map, bricks));
  const { dependencies, supporting } = getDependencies(map, current);

  return Object.entries(dependencies).reduce((acc, [id, deps]) => {
    for (const dep of deps) {
      if (wouldFall(supporting, dep, [Number(id)])) {
        return acc;
      }
    }
    return acc + 1;
  }, 0);
}

const getChain = (dependencies: Record<number, number[]>, supporting: Record<number, number[]>, id: number, bricks: number[]): number[] => {
  if (bricks.includes(id)) {
    return bricks;
  }

  if (wouldFall(supporting, id, bricks)) {
    bricks.push(id);

    for (const dep of dependencies[id]) {
      bricks = getChain(dependencies, supporting, dep, bricks);
    }
  }

  return bricks;
};

const partB = () => {
  let current: BrickType[] = [...bricks];
  let map = generateMap(bricks);
  ({ map, bricks: current } = settle(map, bricks));
  const { dependencies, supporting } = getDependencies(map, current);

  return Object.entries(dependencies).reduce((acc, [id, deps]) => {
    const idNumber = Number(id);
    let fell: number[] = [idNumber];

    for (const dep of deps) {
      fell = getChain(dependencies, supporting, dep, fell);
    }

    const test = new Set(fell);
    if (fell.length !== test.size) {
      console.log(fell);
      console.log(test);
    }
    return acc + fell.length - 1;
  }, 0);
}

console.log('Part A:', partA());
console.log('Part B:', partB());
