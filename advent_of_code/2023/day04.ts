import { readInput } from "./utils";

const re = /\d+/g;
const data = readInput((data) => data.split('\n')
  .map((line) => line.split(':')[1]
    .split('|')
    .map((nums) => [...nums.matchAll(re)]
      .map((match) => Number(match[0]))
))) as number[][][];

const getWinnerCount = (winners: number[], mine: number[]) => mine.filter((num) => winners.includes(num)).length;

const partA = () => {
  return data.reduce((total, [winners, mine]) => {
    const matching = getWinnerCount(winners, mine);
    return matching ? total + (2 ** (matching - 1)) : total;
  }, 0);
}

const partB = () => {
  const copies: Record<number, number> = {};

  return data.reduce((acc, [winners, mine], id) => {
    const matching = getWinnerCount(winners, mine);
    if (!(id in copies)) {
      copies[id] = 1;
    }

    for (let i = id + 1; i < id + 1 + matching; i++) {
      copies[i] = (copies[i] ?? 1) + copies[id];
    }

    return acc + (matching * copies[id]);
  }, data.length);
}

console.log('Part A:', partA());
console.log('Part B:', partB());