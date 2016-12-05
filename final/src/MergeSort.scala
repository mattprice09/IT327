package src

import scala.collection.mutable.ArrayBuffer;

class MergeSort() {

  def merge(l: ArrayBuffer[Int], r: ArrayBuffer[Int]): ArrayBuffer[Int] = {
    var out = ArrayBuffer[Int]();

    var lx = 0;
    var rx = 0;
    while (lx < l.length && rx < r.length) {
      if (l(lx) < r(rx)) {
        out += l(lx);
        lx += 1;
      } else {
        out += r(rx);
        rx += 1;
      }
    }

    while (lx < l.length) {
      out += l(lx);
      lx += 1;
    }
    while (rx < r.length) {
      out += r(rx);
      rx += 1;
    }
    return out;
  }

  def sort(xs: ArrayBuffer[Int]) : ArrayBuffer[Int] = {
    if (xs.length == 1) {
      return xs;
    }

    val pivot = xs.length / 2;
    var (l, r) = xs.splitAt(pivot);
    return mergeIterative(sortIterative(l), sortIterative(r));
  }
}
