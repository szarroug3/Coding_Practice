const fs = require('fs');

function readFile(
  separator = null,
  lineCallBack = null,
  lineSeparator = null,
  linePieceCallBack = null
) {
  if (process.argv.length < 3) {
    throw new Error('Input filename required.');
  }
  if (process.argv.length > 3) {
    throw new Error('Only one input argument expected.');
  }

  let data = fs.readFileSync(process.argv[2], 'utf8').trim();
  if (separator == null) {
    return data;
  }

  data = data.split(separator);
  if (lineCallBack != null) {
    data = data.map((line) => lineCallBack(line));
  }
  if (lineSeparator == null) {
    return data;
  }

  return data.map((line) => {
    pieces = line.split(lineSeparator);
    if (linePieceCallBack != null) {
      pieces = pieces.map((piece) => linePieceCallBack(piece));
    }
    return pieces;
  });
}

module.exports = { readFile };
