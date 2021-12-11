import static org.junit.Assert.assertEquals;

import java.io.FileNotFoundException;
import java.io.IOException;
import org.junit.Test;

/**
 * Unit test for Day 4 of AOC 2021.
 */
public class Day04Test {

  /**
   * Make sure part A runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partOneTest() throws FileNotFoundException, IOException {
    int result = new Day04("resources/day04.txt").partOne();
    assertEquals(4512, result);
  }

  /**
   * Make sure part B runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partTwoTest() throws FileNotFoundException, IOException {
    int result = new Day04("resources/day04.txt").partTwo();
    assertEquals(1924, result);
  }
}