import { readInput } from './utils';

const data = readInput((data) => data.split(',')) as string[];
type LensType = { label: string; focal: number };

const hash = (step: string) => {
  return step.split('').reduce((acc, char) => {
    acc += char.charCodeAt(0);
    acc *= 17;
    return acc % 256;
  }, 0);
};

const partA = () => {
  return data.reduce((acc, step) => acc + hash(step), 0);
};

const hashmap = (boxes: Record<number, Array<LensType>>, instruction: string) => {
  const operation = instruction.includes('=') ? '=' : '-';
  const split = instruction.includes('=') ? instruction.split('=') : instruction.split('-');
  const label = split[0];
  const focal = Number(split[1]);
  const box = hash(label);

  if (!(box in boxes)) {
    boxes[box] = [];
  }
  const index = boxes[box].findIndex(value => value.label === label);

  if (operation === '=') {
    if (index !== -1) {
      boxes[box][index] = { label, focal };
    } else {
      boxes[box].push({ label, focal });
    }
  } else if (box in boxes) {
    if (index !== -1) {
      boxes[box].splice(index, 1);
    }
  }

  return boxes;
};

const partB = () => {
  let boxes: Record<number, Array<LensType>> = {};
  for (const step of data) {
    boxes = hashmap(boxes, step);
  }

  return Object.entries(boxes).reduce((acc, [box, values]) => {
    const boxValue = Number(box) + 1;
    values.forEach((lens, index) => {
      acc += boxValue * lens.focal * (index + 1);
    });
    return acc;
  }, 0);
};

console.log('Part A:', partA());
console.log('Part A:', partB());