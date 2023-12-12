import { readInput } from "./utils";

type Node = {
  curr: string;
  steps: number;
  direction: number;
};
type Shortcuts = {
  [key: string]: {
    [key: number]: {
      end: string;
      steps: number;
    }
  }
};

const { directions, map } = readInput((data) => {
  const re = /((.*) = \((.*), (.*)\))/g;
  const lines = data.split('\n');
  const directions = lines[0].split('');
  const map = lines.slice(2).reduce((acc, line) => {
    const [source, left, right] = [...line.matchAll(re)][0].slice(2);

    return {
      ...acc,
      [source]: {
        L: left,
        R: right
      },
    }
  }, {});
  return { directions, map };
}) as { directions: string[], map: Record<string, Record<string, string>> };

const partA = () => {
  const shortcuts: {[key: string]: {steps: number, end: string}} = {};
  let curr = 'AAA';
  let steps = 0;

  while (curr !== 'ZZZ') {
    if (curr in shortcuts) {
      steps += shortcuts[curr].steps;
      curr = shortcuts[curr].end;
      break;
    }

    const start = curr;
    let currSteps = 0;

    for (let i = 0; i < directions.length && curr !== 'ZZZ'; i++) {
      const next = map[curr][directions[i]];
      curr = next;
      steps++;
      currSteps++;
    }
    shortcuts[start] = { steps: currSteps, end: curr };
  }
  return steps;
};

const getZ = (node: Node, shortcuts: Shortcuts) => {
  const visited = [];

  do {
    if (node.curr in shortcuts && node.direction in shortcuts[node.curr]) {
      const curr = node.curr;
      const direction = node.direction;
      node.steps += shortcuts[curr][direction].steps;
      node.direction = (direction + shortcuts[curr][direction].steps) % directions.length;
      node.curr = shortcuts[curr][direction].end;
    } else {
      visited.push({
        node: node.curr,
        direction: node.direction,
        steps: node.steps
      });

      node.curr = map[node.curr][directions[node.direction]];
      node.steps++;
      node.direction = (node.direction + 1) % directions.length;
    }
  } while (node.direction !== 0 || !node.curr.endsWith('Z'));

  for (const visit of visited) {
    if (!(visit.node in shortcuts)) {
      shortcuts[visit.node] = {};
    }
    shortcuts[visit.node][visit.direction] = {
      end: node.curr,
      steps: node.steps - visit.steps,
    };
  }

  return { z: node.steps, shortcuts };
};

const partB = () => {
  let shortcuts: Shortcuts = {};
  const nodes = Object.keys(map).filter((node) => node.endsWith('A')).reduce((acc, node) => {
    return {
      ...acc,
      [node]: { curr: node, steps: 0, direction: 0 }
    };
  }, {} as Record<string, Node>);

  const values = Object.values(nodes).reduce((acc, node) => {
    const result = getZ(node, shortcuts);
    shortcuts = result.shortcuts;
    return [...acc, result.z];
  }, [] as number[]);
 
  for (let i = 2; i < Math.floor(Math.min(...values) / 2); i++) {
    if (!(6 * i - 1) && !(6 * i + 1)) {
      continue;
    }
    if (values.every((value) => value % i === 0)) {
      return values.reduce((acc, value) => acc * (value / i), i);
    }
  }
};

console.log('Part A:', partA());
console.log('Part B:', partB());