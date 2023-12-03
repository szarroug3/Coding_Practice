import { readInput } from "./utils.js";

const data = readInput((data) => data.split('\n'));
  const numRe = /\d+/g;
const symbolRe = /[^.0-9]/g;

const getSurroundingMatches = (re, { row, col, length=1 }) => {
  const matches = [];

  const startingRow = row > 0 ? row - 1 : row;
  const endingRow = row + 1 < data.length ? row + 1 : row;
  const startingCol = col > 0 ? col - 1 : col;
  const endingCol = col + length < data[row].length ? col + length + 1 : col + length;

  for (let i = startingRow; i <= endingRow; i++) {
    const curr = [...data[i].slice(startingCol, endingCol).matchAll(re)].map((match) => {
      return {
        row: i,
        col: startingCol + match.index,
        val: match[0],
      }
    });
    matches.push(...curr);
  }

  return matches;
};

const partA = () => {
  const numbers = data.reduce((acc, line, index) => {
    const matches = [...line.matchAll(numRe)];
    numRe.lastIndex = 0;
    if (!matches.length) {
      return acc;
    }

    return [...acc, ...matches.map((match) => {
      return {
        row: index,
        col: match.index,
        length: match[0].length,
        val: Number(match[0])
      }
    })];
  }, []);

  return numbers.reduce((total, num) => {
    return total + (getSurroundingMatches(symbolRe, num).length ? num.val: 0);
  }, 0);
};

const partB = () => {
  const symbols = data.reduce((acc, line, index) => {
    const matches = [...line.matchAll(symbolRe)];
    numRe.lastIndex = 0;
    if (!matches.length) {
      return acc;
    }

    return [...acc, ...matches.map((match) => {
      return {
        row: index,
        col: match.index,
        length: match[0].length,
        val: match[0]
      }
    })];
  }, []);

  return symbols.reduce((total, symbol) => {
    const matches = [...getSurroundingMatches(numRe, symbol)];
    if (matches.length == 2) {
      return total + matches.reduce((acc, { row, col, val }) => {
        let newCol = col + val.length;
        while (newCol < data[row].length && data[row][newCol].match(numRe)) {
          val = val + data[row][newCol];
          newCol++;
        }

        newCol = col - 1;
        while (newCol >= 0 && data[row][newCol].match(numRe)) {
          val = data[row][newCol] + val;
          newCol--;
        }

        return acc * Number(val);
      }, 1);
    }
    return total;
  }, 0);
};

console.log('Part A: ', partA());
console.log('Part B: ', partB());
