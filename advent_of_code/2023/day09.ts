import { readInput } from "./utils";

const data = readInput((data) => {
  return data.split('\n').map((line) => line.split(' ').map(Number));
}) as number[][];

const partA = () => {
  return data.reduce((acc, line) => {
    const subtractions = [line];
    while (subtractions[subtractions.length - 1].some((x) => x !== 0)) {
      subtractions.push(subtractions[subtractions.length - 1].slice(1).map((x, i) => x - subtractions[subtractions.length - 1][i]));
    }

    subtractions[subtractions.length - 1].push(0);

    for (let i = subtractions.length - 2; i >= 0; i--) {
      subtractions[i].push(subtractions[i+1][subtractions[i+1].length - 1] + subtractions[i][subtractions[i].length - 1]);
    }
    return acc + subtractions[0][subtractions[0].length - 1];
  }, 0);
};

const partB = () => {
  return data.reduce((acc, line) => {
    const subtractions = [line];
    while (subtractions[subtractions.length - 1].some((x) => x !== 0)) {
      subtractions.push(subtractions[subtractions.length - 1].slice(1).map((x, i) => x - subtractions[subtractions.length - 1][i]));
    }

    subtractions[subtractions.length - 1].unshift(0);

    for (let i = subtractions.length - 2; i >= 0; i--) {
      subtractions[i].unshift(subtractions[i][0] - subtractions[i+1][0]);
    }
    return acc + subtractions[0][0];
  }, 0);
};

console.log('Part A:', partA());
console.log('Part B:', partB());