import {
  readInput
} from './utils';

type handType = {
  bid: number;
  value: number;
  wildValue: number;
}
const cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'];
const wildCards = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'];

const types = [
  [1, 1, 1, 1, 1],
  [1, 1, 1, 2],
  [1, 2, 2],
  [1, 1, 3],
  [2, 3],
  [1, 4],
  [5]
];

const wildMap: Record < number, number > = {
  1: 1,
  2: 2,
  3: 3,
  4: 4,
  5: 4,
  6: 5,
  7: 5
};

const getValue = (hand: string[], cards: string[]) => {
  return hand.map((value) => {
    let index = String(cards.indexOf(value));
    if (index.length == 1) {
      index = `0${index}`;
    }
    return index;
  }).join('');
};

const getCounts = (hand: string[]) => {
  return hand.reduce((acc, card) => {
    return {
      ...acc,
      [card]: (acc[card] ?? 0) + 1
    };
  },
    {} as Record < string,
    number >);
};

const getType = (counts: Record < string, number >) => {
  const sorted = Object.values(counts).sort();
  return types.findIndex((handType) =>
    handType.length === sorted.length && handType.every((val, index) => val === sorted[index])
  ) + 1;
};

const getWildType = (counts: Record < string, number >) => {
  const jokers = counts.J;
  if (jokers === 5 || !('J' in counts)) {
    return getType(counts);
  }

  const {
    J,
    ...values
  } = counts;
  const max = Object.entries(values).sort((a, b) => b[1] - a[1]).map(([card]) => card)[0];
  values[max] += jokers;
  return getType(values);
}

const data = readInput((data) => {
  const re = /(\w)(\w)(\w)(\w)(\w) (\d+)/g;
  return data.split('\n').map((line) => {
    const match = Array.from(line.matchAll(re))[0];
    const hand = match.slice(1, 6);
    const counts = getCounts(hand);

    const type = getType(counts);
    const value = getValue(hand, cards);

    const wildValue = getValue(hand, wildCards);
    const wildType = getWildType(counts);

    return {
      bid: Number(match[6]),
      value: Number(`${type}${value}`),
      wildValue: Number(`${wildType}${wildValue}`),
    };
  });
}) as handType[];

const partA = (): number => {
  return data.sort((a, b) => a.value - b.value)
  .reduce((acc, {
    bid
  }, index) => acc + (bid * (index + 1)), 0);
};

const partB = () => {
  return data.sort((a, b) => a.wildValue - b.wildValue)
  .reduce((acc, {
    bid
  }, index) => acc + (bid * (index + 1)), 0);
};

console.log('Part A:',
  partA());
console.log('Part B:',
  partB());