package src

class Point(val xc: Int, val yc: Int) {
  var x: Int = xc
  var y: Int = yc

  def printCoords() {
    println ("X: " + x);
    println ("Y: " + y);
  }
   
  def move(dx: Int, dy: Int) {
    x = x + dx
    y = y + dy
    println ("Point x location : " + x);
    println ("Point y location : " + y);
  }
}
