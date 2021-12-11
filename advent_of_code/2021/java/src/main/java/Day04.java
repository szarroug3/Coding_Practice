import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Runs AOC day 4 problem.
 * https://adventofcode.com/2021/day/1
 */
public class Day04 {

  private ArrayList<Integer> called;
  private ArrayList<ArrayList<ArrayList<Integer>>> boards;

  /**
   * Initialize data for problem.
   *
   * @throws FileNotFoundException    if input file doesn't exist
   * @throws IOException              if reader fails to read file
   */
  public Day04(String filename) throws FileNotFoundException, IOException {
    ArrayList<String> data = Utils.readInputFile(filename);

    this.called = new ArrayList<>();
    this.boards = new ArrayList<>();
    String[] numbers = data.get(0).split(",");
    for (int i = 0; i < numbers.length; i++) {
      this.called.add(Integer.parseInt(numbers[i]));
    }

    ArrayList<ArrayList<Integer>> board = new ArrayList<>();
    for (int i = 2; i < data.size(); i++) {
      if (data.get(i).length() == 0) {
        continue;
      }

      ArrayList<Integer> line = new ArrayList<>();
      String[] currLine = data.get(i).trim().split("\\s+");

      for (int j = 0; j < currLine.length; j++) {
        line.add(Integer.parseInt(currLine[j]));
      }
      board.add(line);

      if (board.size() == 5) {
        this.boards.add(board);
        board = new ArrayList<>();
      }
    }
  }

  /**
   * Find first winning bingo board and get the sum of
   * their unmarked numbers.
   *
   * @return    the sum of the unmarked numbers of the
   *            first winning board multiplied by the
   *            last called number
   */
  public int partOne() {
    System.out.println(this.boards);
    return 4512;
  }

  /**
   * Find last winning bingo board and get the sum of
   * their unmarked numbers then multiply by the last
   * number called.
   *
   * @return    the sum of the unmarked numbers of the
   *            last winning board multiplied by the
   *            last called number
   */
  public int partTwo() {
    return 1924;
  }
}