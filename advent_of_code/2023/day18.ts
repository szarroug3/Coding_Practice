import { readInput } from "./utils";

type DirectionType = {
  direction: string;
  distance: number;
  color?: string;
}

const data = readInput((data) => {
  const re = /(R|D|L|U) (\d+) \((#[a-f0-9]+)\)/;
  return data.split('\n').map((line) => {
    const matches = re.exec(line)!;
    return { direction: matches[1], distance: Number(matches[2]), color: matches[3] };
  });
}) as DirectionType[];

const directions: Record<string, number[]> = {
  R: [1, 0],
  D: [0, 1],
  L: [-1, 0],
  U: [0, -1],
};

const colorToDirection: Record<string, string> = {
  0: 'R',
  1: 'D',
  2: 'L',
  3: 'U',
}

const getVertices = (data: DirectionType[] ) => {
  const vertices = [[0, 0]];
  let x = 0;
  let y = 0;

  for (const { direction, distance } of data) {
    const [dx, dy] = directions[direction];

    x += dx * distance;
    y += dy * distance;

    vertices.push([x, y]);
  }

  return vertices;
};

const getArea = (data: DirectionType[]) => {
  const vertices = getVertices(data);
  let area = 0;

  for (let i = 0; i < vertices.length - 1; i++) {
    const [x0, y0] = vertices[i];
    const [x1, y1] = vertices[i + 1];
    area += (x0 * y1) - (x1 * y0);
  }

  area = Math.abs(area / 2);
  let perimeter = data.reduce((acc, { distance }) => acc + distance, 0);
  return Math.ceil(area - (perimeter / 2) + 1) + perimeter;
}

const partA = () => {
  return getArea(data);
};

const getCorrectedInstructions = () => {
  const directions = [];

  for (const { color } of data) {
    const direction = colorToDirection[color!.slice(-1)];
    const distance = parseInt(color!.slice(1, color!.length - 1), 16);
    directions.push({ direction, distance });
  }

  return directions;
}

const partB = () => {
  const corrected = getCorrectedInstructions();
  return getArea(corrected);
};

console.log('Part A: ', partA());
console.log('Part B: ', partB());