package src

import scala.collection.mutable.ArrayBuffer;

class QuickSort() {

  // Functional programming implementation of QuickSort
  def sortFunctional(list: List[Int]): List[Int] = {
    list match {
      case Nil => Nil
      case pivot :: tail => {
        val (less, greater) = tail.partition(_ < pivot)
        sortFunctional(less) ::: pivot :: sortFunctional(greater)
      }
    }
  }

  // Functional programming implementation using foldLeft.
  // @author Daniel Spiewak
  def sortFunctionalFL[A : Ordering](ls: List[A]) = {
    import Ordered._

    def sort(ls: List[A])(parent: List[A]): List[A] = {
      if (ls.size <= 1) ls ::: parent else {
        val pivot = ls.head

        val (less, equal, greater) = ls.foldLeft((List[A](), List[A](), List[A]())) {
          case ((less, equal, greater), e) => {
            if (e < pivot)
              (e :: less, equal, greater)
            else if (e == pivot)
              (less, e :: equal, greater)
            else
              (less, equal, e :: greater)
          }
        }

        sort(less)(equal ::: sort(greater)(parent))
      }
    }
    sort(ls)(Nil)
  }

  // QuickSort using iterative approach (in-place)
  def sortIterative(list:ArrayBuffer[Int]):ArrayBuffer[Int] = {
    // Base case
    if (list.length <= 1) {
      return list;
    }

    val pivot = list(list.length-1);

    // 'n' to keep track of the size of > chunk
    var i = 0;
    var n = 1;
    for (i <- 0 until list.length) {
      if (list(i) > pivot) {
        while (i+n < list.length && list(i+n) > pivot) {
          n += 1;
        }
        if (i+n < list.length) {
          val tmp = list(i+n);
          list(i+n) = list(i);
          list(i) = tmp;
        }
      }
    }

    // Split at the partition, sort the left and right sides. 
    var (left, right) = list.splitAt(list.indexOf(pivot));
    right -= pivot;
    left = sortIterative(left);
    right = sortIterative(right);

    // Combine results and return
    left += pivot;
    left.appendAll(right);
    return left;
  }
}
