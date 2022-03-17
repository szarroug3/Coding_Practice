// https://adventofcode.com/2020/day/9

const { readFile } = require('../utils/input');

function breakXMASEncryption(data) {
  let invalidValue = findInvalidValue(data);
  let encryptionWeakness = findEncryptionWeakness(data, invalidValue);
  return [invalidValue, encryptionWeakness];
}

function findInvalidValue(data) {
  let preambleLength = 25;

  for (let i = preambleLength; preambleLength < data.length; i++) {
    if (!checkValue(data.slice(i - preambleLength, i), data[i])) {
      return data[i];
    }
  }
}

function checkValue(data, value) {
  for (let i = 0; i < data.length - 1; i++) {
    for (let j = i + 1; j < data.length; j++) {
      if (data[i] + data[j] == value) {
        return true;
      }
    }
  }
  return false;
}

function findEncryptionWeakness(data, value) {
  for (let i = 0; i < data.length; i++) {
    let resultIndex = checkForSum(data, i, value);
    if (resultIndex != -1) {
      let values = data.slice(i, resultIndex + 1);
      let min = Math.min(...values);
      let max = Math.max(...values);
      return min + max;
    }
  }
}

function checkForSum(data, index, value) {
  let sum = 0;
  for (let i = index; i < data.length; i++) {
    sum += data[i];
    if (sum == value) {
      return i;
    } else if (sum > value) {
      return -1;
    }
  }
  return -1;
}

function main() {
  try {
    var data = readFile('\n', parseInt);
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let answers = breakXMASEncryption(data);
  console.log(`Part A: ${answers[0]}`);
  console.log(`Part B: ${answers[1]}`);
}

main();
