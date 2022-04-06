// https://adventofcode.com/2020/day/16

const { readFile } = require('../utils/input');

function parse(data) {
  let parsed = { fields: {}, nearby: [] };

  let i = 0;
  fieldRe = /(.*): (\d+)-(\d+) or (\d+)-(\d+)/;
  for (; data[i] != ''; i++) {
    let matches = data[i].match(fieldRe);
    let values = [];
    for (let j = 2; j < matches.length; j += 2) {
      values.push([parseInt(matches[j]), parseInt(matches[j + 1])]);
    }
    parsed['fields'][matches[1]] = values;
  }

  i += 2;
  parsed['yours'] = Array.from(data[i].split(','), (val) => parseInt(val));

  for (i += 3; i < data.length; i++) {
    parsed['nearby'].push(
      Array.from(data[i].split(','), (val) => parseInt(val))
    );
  }

  return parsed;
}

function process(data) {
  invalid = [];
  valid = [];
  data['nearby'].forEach((ticket) => {
    let currInvalid = ticket.filter((value) => !isValid(value, data['fields']));
    invalid.push(...currInvalid);

    if (currInvalid.length == 0) {
      valid.push(ticket);
    }
  });
  let errorRate = invalid.reduce((count, value) => count + value, 0);

  let fields = Object.keys(data['fields']);
  let order = [];
  for (let i = 0; i < data['yours'].length; i++) {
    order.push(fields.slice());
  }

  let complete = [];
  valid.forEach((ticket) => {
    for (let i = 0; i < ticket.length; i++) {
      order[i] = getPossibleFields(ticket[i], data['fields'], order[i]);
      if (order[i].length == 1 && !complete.includes(order[i][0])) {
        complete.push(order[i][0]);
      }
    }
  });

  let done = false;
  while (!done) {
    done = true;
    for (let i = 0; i < order.length; i++) {
      if (order[i].length == 1) {
        continue;
      }
      done = false;

      let length = order[i].length;
      order[i] = order[i].filter((value) => !complete.includes(value));

      if (order[i].length == 1) {
        complete.push(order[i][0]);
      }
    }
  }

  let product = 1;
  for (let i = 0; i < order.length; i++) {
    if (order[i][0].startsWith('departure')) {
      product *= data['yours'][i];
    }
  }

  return [errorRate, product];
}

function isValid(value, fields) {
  return Object.values(fields).some((values) => {
    return values.some((range) => {
      if (value >= range[0] && value <= range[1]) {
        return true;
      }
    });
  });
}

function getPossibleFields(value, fields, allowed) {
  return allowed.filter((field) => {
    return fields[field].some((range) => {
      if (value >= range[0] && value <= range[1]) {
        return true;
      }
    });
  });
}

function main() {
  try {
    var data = parse(readFile('\n'));
  } catch (error) {
    console.log(error.message);
    process.exit();
  }

  let [partA, partB] = process(data);
  console.log(`Part A: ${partA}`);
  console.log(`Part B: ${partB}`);
}

main();
