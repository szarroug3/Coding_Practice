import { readInput } from './utils';

const { times, distances } = readInput((data) => {
  const re = /(\d+)/g;
  const lines = data.split('\n');
  const times = lines[0].match(re)!.map(Number);
  const distances = lines[1].match(re)!.map(Number);
  return { times, distances };
}) as Record<string, number[]>;

const partA = () => {
  let result = 1;

  for (let i = 0; i < times.length; i++) {
    const time = times[i];
    const distance = distances[i] + 1;

    const possibilities = [
      (time + Math.sqrt((time * time) - (4 * (distance)))) / 2,
      (time - Math.sqrt((time * time) - (4 * (distance)))) / 2
    ].sort((a, b) => a - b);

    result *= Math.floor(possibilities[1]) - Math.ceil(possibilities[0]) + 1;
  }

  return result;
};

const partB = () => {
  const time = Number(times.map(String).join(''));
  const distance = Number(distances.map(String).join(''));

  const possibilities = [
    (time + Math.sqrt((time * time) - (4 * (distance)))) / 2,
    (time - Math.sqrt((time * time) - (4 * (distance)))) / 2
  ].sort((a, b) => a - b);

  return Math.floor(possibilities[1]) - Math.ceil(possibilities[0]) + 1;
};

console.log('Part A:', partA());
console.log('Part B:', partB());