import java.util.HashMap;
import java.util.Map;

/**
* Program that mimics the rough concept of what activation records do.
*
* Ignored "Return Address"
* 
* @author Matt Price
*/

public class f {

  // Represents `fun g` from ML example
  private int g(Map<String, Object> prevRecord, int n) {
    if (n == 0) {
      // base case
      return 0;
    }
    int a = (int)(prevRecord.get("x")) + (int)(prevRecord.get("y"));

    // Create record for this activation
    Map<String, Object> record = new HashMap<String, Object>() {{
      put("a", a);
      put("n", n);
      put("nestingLink", prevRecord);
    }};
    return this.h(record, n-1);
  }

  // Represents `fun h` from ML example
  @SuppressWarnings("unchecked")
  private int h(Map<String, Object> prevRecord, int k) {
    if (k == 0) {
      // base case
      return 0;
    }
    return (int)(prevRecord.get("a")) + (int)(prevRecord.get("n")) + this.g((Map<String, Object>)(prevRecord.get("nestingLink")), (int)(prevRecord.get("n"))-1);
  }

  // The main function to run computations
  // Represents `fun f` from ML example
  public int compute(int x, int y) {
    int a = x+1;

    // Create record for this activation
    Map<String, Object> record = new HashMap<String, Object>() {{
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
    int val = fObj.compute(x, y);
    System.out.println("f(" + x + ", " + y + ")=" + val);
  }
}
