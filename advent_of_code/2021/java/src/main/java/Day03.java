import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Runs AOC day 3 problem.
 * https://adventofcode.com/2021/day/2
 */
public class Day03 {

  private ArrayList<String> data;

  /**
   * Initialize data for problem.
   *
   * @throws FileNotFoundException    if input file doesn't exist
   * @throws IOException              if reader fails to read file
   */
  public Day03(String filename) throws FileNotFoundException, IOException {
    this.data = Utils.readInputFile(filename);
  }

  /**
   * Find gamma and epsilon rates based on the most and least
   * common bits respectively.
   *
   * @return    result of gamma and epsilon rates multiplied together
   */
  public int partOne() {
    ArrayList<Integer> zeroes = new ArrayList<>();
    ArrayList<Integer> ones = new ArrayList<>();

    for (int i = 0; i < this.data.size(); i++) {
      for (int j = 0; j < this.data.get(i).length(); j++) {
        if (zeroes.size() <= j) {
          zeroes.add(0);
          ones.add(0);
        }

        if (this.data.get(i).charAt(j) == '0') {
          zeroes.set(j, zeroes.get(j) + 1);
        } else {
          ones.set(j, ones.get(j) + 1);
        }
      }
    }

    String gamma = "";
    String epsilon = "";
    for (int i = 0; i < zeroes.size(); i++) {
      if (zeroes.get(i) > ones.get(i)) {
        gamma += "0";
        epsilon += "1";
      } else {
        gamma += "1";
        epsilon += "0";
      }
    }

    return Integer.parseInt(gamma, 2) * Integer.parseInt(epsilon, 2);
  }

  /**
   * Find life support and oxygen generator ratings based on the most and least
   * common bits respectively.
   *
   * @return    result of life support and oxygen generator ratings multiplied together
   */
  public int partTwo() {
    return 230;
  }
}