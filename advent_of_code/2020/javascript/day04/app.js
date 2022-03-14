// https://adventofcode.com/2020/day/4

const { readFile } = require('../utils/input');

function parse(data) {
  let passports = [];
  let curr = {};
  data.forEach((element) => {
    if (element == '') {
      passports.push(curr);
      curr = {};
    } else {
      let data = element.split(' ');
      data.forEach((element) => {
        let values = element.split(':');
        curr[values[0]] = values[1];
      });
    }
  });

  // push the last passport since it won't get pushed by the loop
  passports.push(curr);

  return passports;
}

function validate(passport, onlyCheckFields) {
  const required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'];
  let result = required.every((requirement) => requirement in passport);
  if (!result || onlyCheckFields) {
    if (!onlyCheckFields) {
    }
    return result;
  }

  // byr (Birth Year) - four digits; at least 1920 and at most 2002.
  if (isNaN(passport.byr) || passport.byr < 1920 || passport.byr > 2002) {
    return false;
  }

  // iyr (Issue Year) - four digits; at least 2010 and at most 2020.
  if (isNaN(passport.iyr) || passport.iyr < 2010 || passport.iyr > 2020) {
    return false;
  }

  // eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
  if (isNaN(passport.eyr) || passport.eyr < 2020 || passport.eyr > 2030) {
    return false;
  }

  // hgt (Height) - a number followed by either cm or in:
  //     If cm, the number must be at least 150 and at most 193.
  //     If in, the number must be at least 59 and at most 76.
  let heightType = passport.hgt.substr(passport.hgt.length - 2, 2);
  if (heightType != 'cm' && heightType != 'in') {
    return false;
  }
  let height = passport.hgt.substr(0, passport.hgt.length - 2);
  if (isNaN(height)) {
    return false;
  }
  height = parseInt(height);
  if (heightType == 'cm' && (height < 150 || height > 193)) {
    return false;
  }
  if (heightType == 'in' && (height < 59 || height > 76)) {
    return false;
  }

  // hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
  if (passport.hcl.length != 7 || passport.hcl[0] != '#') {
    return false;
  }
  const hexColors = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
  ];
  for (let i = 1; i < passport.hcl.length; i++) {
    if (!hexColors.includes(passport.hcl[i])) {
      return false;
    }
  }

  // ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
  const colors = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'];
  if (!colors.includes(passport.ecl)) {
    return false;
  }

  // pid (Passport ID) - a nine-digit number, including leading zeroes.
  if (passport.pid.length != 9 || isNaN(passport.pid)) {
    return false;
  }

  return true;
}

async function partA(data) {
  return new Promise((resolve) => {
    resolve(data.filter((element) => validate(element, true)).length);
  });
}

async function partB(data) {
  return new Promise((resolve) => {
    resolve(data.filter((element) => validate(element, false)).length);
  });
}

async function main() {
  try {
    var data = parse(readFile('\n'));
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let answers = await Promise.all([partA(data), partB(data)])
    .then((answers) => {
      console.log(`Part A: ${answers[0]}`);
      console.log(`Part B: ${answers[1]}`);
    })
    .catch(console.log);
}

main();
