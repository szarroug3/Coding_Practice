import java.io.FileNotFoundException;
import java.io.IOException;

/**
 * Run code for Advent of Code.
 */
public class Aoc {

  /**
   * Read input from Advent of Code problems and report results.
   *
   * @param args  input to main
   */
  public static void main(String[] args) {
    try {
      Day01 day01 = new Day01("day01.txt");
      System.out.printf("Part A: %s\nPart B: %s\n", day01.partOne(), day01.partTwo());

      Day02 day02 = new Day02("day02.txt");
      System.out.printf("Part A: %s\nPart B: %s\n", day02.partOne(), day02.partTwo());

      Day03 day03 = new Day03("day03.txt");
      System.out.printf("Part A: %s\nPart B: %s\n", day03.partOne(), day03.partTwo());
    } catch (FileNotFoundException e) {
      System.out.println(e.getMessage());
    } catch (IOException e) {
      System.out.println(e);
    }
  }
}
