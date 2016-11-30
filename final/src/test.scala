package src

object test {
  def main(args: Array[String]) {
    println("Hello, world!");
    val p1 = new Point(0, 0);
    p1.printCoords();
    p1.move(-1, 5);
    p1.printCoords();
  }
}
