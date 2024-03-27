import { readInput } from "./utils";

type MapDataType = {
  count: number;
  farthest: number;
  distances: Record<number, string[]>;
}

const { map, start } = readInput(data => {
  const map: string[][] = [];
  let start: number[] = [];

  for (let line of data.split('\n')) {
    const split = line.split('');
    map.push(split);

    if (split.includes('S')) {
      start = [map.length - 1, split.indexOf('S')];
    }
  }

  return { map, start };
}) as { map: string[][], start: number[] };

const getParity = (target: number)  => {
  return target % 2 === 0 ? 'even' : 'odd';
};

const addState = (i: number, j: number, distance: number, visited: string[], queue: number[][]) => {
  const location = `${i},${j}`;
  if (i < 0 || j < 0 || i >= map.length || j >= map[i].length || visited.includes(location) || map[i][j] === '#') {
    return { visited, queue };
  }

  visited.push(location);
  queue.push([i, j, distance]);

  return { visited, queue };
};

const djikstra = (startI: number, startJ: number, target: number, startingCount: number, print?: boolean): Record<string, MapDataType> => {
  let visited: string[] = [`${startI},${startJ}`];
  let queue = [[startI, startJ, startingCount]];
  let evenCount = 0;
  let oddCount = 0;
  let farthestEven = 0;
  let farthestOdd = 0;
  const evenDistances: Record<number, string[]> = {};
  const oddDistances: Record<number, string[]> = {};

  while (queue.length) {
    const [i, j, distance] = queue.shift()!;
    if (distance % 2 === 0) {
      evenCount++;
      if (distance > farthestEven) {
        farthestEven = distance;
      }
      if (!(distance in evenDistances)) {
        evenDistances[distance] = [];
      }
      evenDistances[distance].push(`${i},${j}`);
    } else {
      oddCount++;
      if (distance > farthestOdd) {
        farthestOdd = distance;
      }
      if (!(distance in oddDistances)) {
        oddDistances[distance] = [];
      }
      oddDistances[distance].push(`${i},${j}`);
    }

    if (distance === target) {
      continue;
    }
    
    ({ visited, queue } = addState(i + 1, j, distance + 1, visited, queue));
    ({ visited, queue } = addState(i, j + 1, distance + 1, visited, queue));
    ({ visited, queue } = addState(i - 1, j, distance + 1, visited, queue));
    ({ visited, queue } = addState(i, j - 1, distance + 1, visited, queue));
  }

  return {
    even: {
      count: evenCount,
      farthest: farthestEven,
      distances: evenDistances
    },
    odd: {
      count: oddCount,
      farthest: farthestOdd,
      distances: oddDistances
    }
  };
};

const partA = (target: number) => {
  let parity = getParity(target);
  const data = djikstra(start[0], start[1], target, 0, false);
  return data[parity].count;
};

const processDirections = (
  target: number, firstMapPositiveDelta: boolean, horizontalFirst: boolean, countTurn: boolean,
  distanceToFirstMap: number, directionDistance1: number, directionDistance2: number,
  distances1: Record<string, MapDataType>, direction1: string,
  distances2: Record<string, MapDataType>, turnDistance1: number, direction2: string,
  distances3: Record<string, MapDataType>, turnDistance2: number, direction3: string,
  corner1Distances: Record<string, MapDataType>, distanceToCorner1: number, corner1Direction: string,
  corner2Distances: Record<string, MapDataType>, distanceToCorner2: number, corner2Direction: string,
  edges: Record<string, Record<string, number>>) => {
  let remaining = target - distanceToFirstMap;
  let count = 0;
  let currCount = 0;

  let mapKey1 = 0;

  while (remaining > 0) {
    // going direction 1
    if (firstMapPositiveDelta) {
      mapKey1++;
    } else {
      mapKey1--;
    }
    let parity = getParity(remaining);
    if (horizontalFirst) {
      ({ edges, count: currCount } = processDirection(distances1[parity], remaining, mapKey1, 0, direction1, edges));
    } else {
      ({ edges, count: currCount } = processDirection(distances1[parity], remaining, 0, mapKey1, direction1, edges));
    }
    count += currCount;

    // going direction 2
    let currRemaining = remaining - turnDistance1;
    let mapKey2 = -1;

    let parityCount;
    let parityMapCount;
    if (getParity(directionDistance2) === 'odd') {
      parityCount = distances2.odd.count + distances2.even.count;
      parityMapCount = 2;
    } else {
      parityCount = distances2.even.count;
      parityMapCount = 1;
    }

    let multiplier = Math.floor(currRemaining / (directionDistance2 * parityMapCount));
    if (multiplier) {
      multiplier--;
    }
    if (countTurn) {
      count += parityCount * multiplier;
    }
    mapKey2 -= parityMapCount * multiplier;
    currRemaining -= directionDistance2 * parityMapCount * multiplier;

    while (currRemaining > 0) {
      parity = getParity(currRemaining);
      if (horizontalFirst) {
        ({ edges, count: currCount } = processDirection(distances2[parity], currRemaining, mapKey1, mapKey2, direction2, edges));
      } else {
        ({ edges, count: currCount } = processDirection(distances2[parity], currRemaining, mapKey2, mapKey1, direction2, edges));
      }
      if (countTurn) {
        count += currCount;
      }

      mapKey2--;
      currRemaining -= directionDistance2;
    }

    currRemaining = currRemaining + turnDistance1 - distanceToCorner1;
    if (currRemaining > 0) {
      parity = getParity(currRemaining);
      if (horizontalFirst) {
        ({ edges, count: currCount } = processDirection(corner1Distances[parity], currRemaining, mapKey1, mapKey2, corner1Direction, edges));
      } else {
        ({ edges, count: currCount } = processDirection(corner1Distances[parity], currRemaining, mapKey2, mapKey1, corner1Direction, edges));
      }
    }

    // going direction 3
    currRemaining = remaining - turnDistance2;
    mapKey2 = 1;

    if (getParity(directionDistance2) === 'odd') {
      parityCount = distances3.odd.count + distances3.even.count;
      parityMapCount = 2;
    } else {
      parityCount = distances3.even.count;
      parityMapCount = 1;
    }

    multiplier = Math.floor(currRemaining / (directionDistance2 * parityMapCount));
    if (multiplier) {
      multiplier--;
    }
    if (countTurn) {
      count += parityCount * multiplier;
    }
    mapKey2 += parityMapCount * multiplier;
    currRemaining -= directionDistance2 * parityMapCount * multiplier;

    while (currRemaining > 0) {
      parity = getParity(currRemaining);
      if (horizontalFirst) {
        ({ edges, count: currCount } = processDirection(distances3[parity], currRemaining, mapKey1, mapKey2, direction3, edges));
      } else {
        ({ edges, count: currCount } = processDirection(distances3[parity], currRemaining, mapKey2, mapKey1, direction3, edges));
      }
      if (countTurn) {
        count += currCount;
      }

      mapKey2++;
      currRemaining -= directionDistance2;
    }

    currRemaining = currRemaining + turnDistance2 - distanceToCorner2;
    if (currRemaining > 0) {
      parity = getParity(currRemaining);
      if (horizontalFirst) {
        ({ edges, count: currCount } = processDirection(corner2Distances[parity], currRemaining, mapKey1, mapKey2, corner2Direction, edges));
      } else {
        ({ edges, count: currCount } = processDirection(corner2Distances[parity], currRemaining, mapKey2, mapKey1, corner2Direction, edges));
      }
    }

    remaining -= directionDistance1;
  }

  return { edges, count };
}

const processDirection = (distances: MapDataType, target: number, mapI: number, mapJ: number, direction: string, edges: Record<string, Record<string, number>>) => {
  if (distances.farthest > target) {
    const key = `${mapI},${mapJ}`;
    if (!(key in edges)) {
      edges[key] = {};
    }
    edges[key][direction] = target;

    if ((mapI === 0 && mapJ === 202300) ||
      (mapI === 0 && mapJ === -202300) ||
      (mapJ === 0 && mapI === 202300) ||
      (mapJ === 0 && mapI === -202300)) {
    }
    return { edges, count: 0 }
  }

  return { edges, count: distances.count };
};

const calculateEdge = (targets: Record<string, number>, distances: Record<string, Record<string, MapDataType>>, cache: Record<string, number>) => {
  const key = Object.entries(targets).map(([key, value]) => `${key},${value}`).sort().join(',');
  if (!(key in cache)) {
    const visited: string[] = [];
    for (let [direction, target] of Object.entries(targets)) {
      const parity = getParity(target);
      const data = distances[direction][parity].distances;
      for (let point of Object.entries(data).filter(([distance]) => Number(distance) <= target).flatMap(([_, points]) => points)) {
        if (!visited.includes(point)) {
          visited.push(point);
        }
      }
    }

    cache[key] = visited.length;
  }

  return { cache, count: cache[key] };
};

const partB = (target: number) => {
  const rowLength = map[0].length;
  const colLength = map.length;
  const lastRow = rowLength - 1;
  const lastCol = colLength - 1;

  let startDistances = djikstra(start[0], start[1], target, 0, false);

  const distanceToLeft = start[1];
  const distanceToRight = lastCol - start[1];
  const distanceToBottom = lastRow - start[0];
  const distanceToTop = start[0];

  const rightDistances = djikstra(start[0], 0, target, 1, false);
  const leftDistances = djikstra(start[0], lastCol, target, 1, false);
  const topDistances = djikstra(0, start[1], target, 1, false);
  const bottomDistances = djikstra(lastRow, start[1], target, 1, false);

  const topLeftDistances = djikstra(0, 0, target, 1, false);
  const topRightDistances = djikstra(0, lastRow, target, 1, false);
  const bottomLeftDistances = djikstra(lastCol, 0, target, 1, false);
  const bottomRightDistances = djikstra(lastCol, lastRow, target, 1, false);

  let mapI = 0;
  let mapJ = 0;
  let currCount;

  let parity = getParity(target);
  let { edges, count } = processDirection(startDistances[parity], target, mapI, mapJ, '', {});

  const rightToTop = distanceToLeft + distanceToTop + 1;
  const rightToBottom = distanceToLeft + distanceToBottom + 1;
  ({ edges, count: currCount } = processDirections(
    target, true, false, true,
    distanceToRight, rowLength, colLength,
    rightDistances, 'right',
    topDistances, rightToTop, 'top',
    bottomDistances, rightToBottom, 'bottom',
    topRightDistances, distanceToTop + 1, 'topRight',
    bottomRightDistances, distanceToBottom + 1, 'bottomRight',
    edges));
  count += currCount;

  const leftToTop = distanceToLeft + distanceToTop + 1;
  const leftToBottom = distanceToLeft + distanceToBottom + 1;
  ({ edges, count: currCount } = processDirections(
    target, false, false, true,
    distanceToLeft, rowLength, colLength,
    leftDistances, 'left',
    topDistances, leftToTop, 'top',
    bottomDistances, leftToBottom, 'bottom',
    topLeftDistances, distanceToTop + 1, 'topLeft',
    bottomLeftDistances, distanceToBottom + 1, 'bottomLeft',
    edges));
  count += currCount;

  const bottomToLeft = distanceToBottom + distanceToLeft + 1;
  const bottomToRight = distanceToBottom + distanceToRight + 1;
  ({ edges, count: currCount } = processDirections(
    target, true, true, false,
    distanceToBottom, colLength, rowLength,
    bottomDistances, 'bottom',
    leftDistances, bottomToLeft, 'left',
    rightDistances, bottomToRight, 'right',
    bottomLeftDistances, distanceToLeft + 1, 'bottomLeft',
    bottomRightDistances, distanceToRight + 1, 'bottomRight',
    edges));
  count += currCount;

  const topToLeft = distanceToTop + distanceToLeft + 1;
  const topToRight = distanceToTop + distanceToRight + 1;
  ({ edges, count: currCount } = processDirections(
    target, false, true, false,
    distanceToTop, colLength, rowLength,
    topDistances, 'top',
    leftDistances, topToLeft, 'left',
    rightDistances, topToRight, 'right',
    topLeftDistances, distanceToLeft + 1, 'topLeft',
    topRightDistances, distanceToRight + 1, 'topRight',
    edges));
  count += currCount;

  const distances = {
    right: rightDistances,
    left: leftDistances,
    top: topDistances,
    bottom: bottomDistances,
    topRight: topRightDistances,
    bottomRight: bottomRightDistances,
    topLeft: topLeftDistances,
    bottomLeft: bottomLeftDistances
  };

  let cache: Record<string, number> = {};
  for (let targets of Object.values(edges)) {
    ({ count: currCount, cache } = calculateEdge(targets, distances, cache))
    count += currCount;
  }

  return count;
};

console.log('Part A:', partA(64));
console.log('Part B:', partB(26501365));
