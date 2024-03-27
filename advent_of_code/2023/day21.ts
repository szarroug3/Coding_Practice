import { readInput } from "./utils";

type MapDataType = {
  count: number;
  distances: Record<number, string[]>;
  farthest: number;
}

type MapEdgeDataType = {
  distance: number;
  next: number[];
  mapDelta: number[];
  direction: string;
}

type CacheType = {
  even: MapDataType;
  odd: MapDataType;
  edges: MapEdgeDataType[];
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

const getParity = (target: number): 'even' | 'odd' => {
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

const djikstra = (startI: number, startJ: number, target: number, startingCount: number, print?: boolean): CacheType => {
  let visited: string[] = [`${startI},${startJ}`];
  let queue = [[startI, startJ, startingCount]];

  let evenCount = 0;
  let oddCount = 0;

  let farthestEven = 0;
  let farthestOdd = 0;

  const evenDistances: Record<number, string[]> = {};
  const oddDistances: Record<number, string[]> = {};

  const edges = [];

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

    if (i !== startI) {
      if (i === 0) {
        edges.push({
          distance,
          next: [map.length - 1, j],
          mapDelta: [-1, 0],
          direction: 'down'
        });
      }

      if (i === map.length - 1) {
        edges.push({
          distance,
          next: [0, j],
          mapDelta: [1, 0],
          direction: 'up'
        });
      }
    }

    if (j !== startJ) {
      if (j === 0) {
        edges.push({
          distance,
          next: [i, map[0].length - 1],
          mapDelta: [0, -1],
          direction: 'left'
        });
      }

      if (j === map[0].length - 1) {
        edges.push({
          distance,
          next: [i, 0],
          mapDelta: [0, 1],
          direction: 'right'
        });
      }
    }

    if (distance === target) {
      if (print) {
        console.log(i, j);
      }
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
    },
    edges
  };
};

const partA = (target: number) => {
  let parity = getParity(target);
  const data = djikstra(start[0], start[1], target, 0, false);
  return data[parity].count;
};

const addMapStates = (i: number, j: number, remaining: number, data: CacheType, queue: Array<[mapI: number, mapJ: number, i: number, j: number, distance: number, direction: string]>, visited: string[]) => {
  for (let { distance, next, mapDelta, direction } of data.edges) {
    if (remaining - distance - 1 > 0) {
      const mapI = i + mapDelta[0];
      const mapJ = j + mapDelta[1];
      const mapKey = `${mapI},${mapJ}`;
      if (!visited.includes(mapKey)) {
        queue.push([i + mapDelta[0], j + mapDelta[1], next[0], next[1], remaining - distance - 1, direction]);
      }
    }
  }

  return queue;
};

const partB = (target: number) => {
  const cache: Record<string, CacheType> = {};
  cache[`${start[0]},${start[1]}`] = djikstra(start[0], start[1], target, 0, false);

  const visited: string[] = [];
  const edges: Record<string, Record<string, number>> = {};
  let queue: Array<[mapI: number, mapJ: number, i: number, j: number, distance: number, direction: string]> = [[0, 0, start[0], start[1], target, '']];
  let count = 0;

  while (queue.length) {
    const [mapI, mapJ, i, j, remaining, direction] = queue.shift()!;
    const mapKey = `${mapI},${mapJ}`;

    if (visited.includes(mapKey)) {
      continue;
    }

    const locationKey = `${i},${j}`;
    if (!(locationKey in cache)) {
      cache[locationKey] = djikstra(i, j, target, 0, false);
    }

    const data = cache[locationKey];
    const parity = getParity(remaining);

    if (data[parity].farthest <= remaining) {
      count += data[parity].count;
      visited.push(mapKey);
      queue = queue.filter((data => data[2] !== i || data[3] !== j));
      if (mapKey in edges) {
        delete edges[mapKey];
      }
    } else {
      if (!(mapKey in edges)) {
        edges[mapKey] = {};
      }

      if (!(locationKey in edges[mapKey]) || remaining < edges[mapKey][direction]) {
        edges[mapKey][locationKey] = remaining;
      }
    }

    queue = addMapStates(mapI, mapJ, remaining, data, queue, visited);
    queue = queue.sort((data1, data2) => data1[4] - data2[4])
  }

  const edgeCache: Record<string, number> = {};

  for (let targets of Object.values(edges)) {
    const key = Object.entries(targets).map(([key, value]) => `${key},${value}`).sort().join(',');
    if (!(key in edgeCache)) {
      const visited: string[] = [];
      for (let [locationKey, target] of Object.entries(targets)) {
        const parity = getParity(target);
        const data = cache[locationKey][parity].distances;
        for (let point of Object.entries(data).filter(([distance]) => Number(distance) <= target).flatMap(([_, points]) => points)) {
          if (!visited.includes(point)) {
            visited.push(point);
          }
        }
      }

      edgeCache[key] = visited.length;
    }

    count += edgeCache[key];
  }

  return count;
};

console.log('Part A:', partA(18));
// console.log('Part B:', partB(50));
console.log('Part B:', partB(26501365));
