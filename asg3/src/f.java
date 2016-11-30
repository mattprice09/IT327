import java.util.HashMap;
import java.util.Map;

/**
* Program that mimics the rough concept of what activation records do.
*
* Replaced "Previous Activation Record" field with hard copies of the 
* previous activation record's values. 
*
* Ignored "Return Address"
* 
* @author Matt Price
*/

public class f {

  // Represents `fun g` from ML example
  private int g(Map<String, Integer> prevRecord, int n) {
    if (n == 0) {
      // base case
      return 0;
    }
    int a = prevRecord.get("x") + prevRecord.get("y");

    // Create record for this activation
    Map<String, Integer> record = new HashMap<String, Integer>() {{
      put("a", a);
      put("n", n);
      put("x", prevRecord.get("x"));
      put("y", prevRecord.get("y"));
    }};

    return this.h(record, n-1);
  }

  // Represents `fun h` from ML example
  private int h(Map<String, Integer> prevRecord, int k) {
    if (k == 0) {
      // base case
      return 0;
    }

    return prevRecord.get("a") + prevRecord.get("n") + this.g(prevRecord, prevRecord.get("n")-1);
  }

  // The main function to run computations
  // Represents `fun f` from ML example
  public int compute(int x, int y) {
    int a = x+1;

    // Create record for this activation
    Map<String, Integer> record = new HashMap<String, Integer>() {{
      put("a", a);
      put("x", x);
      put("y", y);
    }};
    
    if (x == 0) {
      // base case
      return this.g(record, y);
    }

    return a + this.g(record, this.compute(x-1, y));
  }

  public static void main(String [] args) {
    if (args.length < 2) {
      System.out.println("ERROR: Invalid input format.");
      System.out.println("Usage: `java f <int> <int>`");
      return;
    }

    int x = Integer.parseInt(args[0]);
    int y = Integer.parseInt(args[1]);

    f fObj = new f();
    for (int i = 0; i < 2; i++) {
      for (int j = 10; j < 21; j++) {
        int val = fObj.compute(i, j);
        System.out.println("f(" + i + ", " + j + ")=" + val);
      }
    }
    
    int val = fObj.compute(x, y);
    System.out.println("f(" + x + ", " + y + ")=" + val);

  }
}
