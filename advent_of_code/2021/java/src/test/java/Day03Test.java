import static org.junit.Assert.assertEquals;

import java.io.FileNotFoundException;
import java.io.IOException;
import org.junit.Test;

/**
 * Unit test for Day 2 of AOC 2021.
 */
public class Day03Test {

  /**
   * Make sure part A runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partOneTest() throws FileNotFoundException, IOException {
    int result = new Day03("resources/day03.txt").partOne();
    assertEquals(198, result);
  }

  /**
   * Make sure part B runs correctly.
   *
   * @throws IOException             if file can't be read
   * @throws FileNotFoundException   if file can't be found
   */
  @Test
  public void partTwoTest() throws FileNotFoundException, IOException {
    int result = new Day03("resources/day03.txt").partTwo();
    assertEquals(230, result);
  }
}
