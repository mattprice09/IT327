package src

import scala.collection.mutable.ArrayBuffer;
import scala.io.Source

object Main {
  def main(args: Array[String]) {

    // Get user input
    println("Please enter the name of your data file:");
    val fileName = scala.io.StdIn.readLine();

    // Read data file
    var list = ArrayBuffer[Int]();
    for (line <- Source.fromFile(fileName).getLines()) {
      list += line.toInt;
    }
    var funcList = list.toList;

    println("> Please enter the type of sort you would like to test:");
    println("1 - MergeSort");
    println("2 - QuickSort");
    var sType = scala.io.StdIn.readLine();
    if (sType == "1") {
      val sorter = new MergeSort();

      var i = 0;
      for (i <- 1 to 5) {
        println("> Running test # " + i + "...");

        var start = System.nanoTime;
        sorter.sort(list);
        println("Time taken for iterative: " + ((System.nanoTime - start) / 1000000000.0));
      }

    } else if (sType == "2") {
      val sorter = new QuickSort();

      var i = 0;
      for (i <- 1 to 5) {
        println("> Running test # " + i + "...");

        var start = System.nanoTime;
        sorter.sortFunctionalFL(funcList);
        println("Time taken for functional (using fold left): " + ((System.nanoTime - start) / 1000000000.0));

        start = System.nanoTime;
        sorter.sortFunctional(funcList);
        println("Time taken for functional (without using fold left): " + ((System.nanoTime - start) / 1000000000.0));

        start = System.nanoTime;
        sorter.sortIterative(list);
        println("Time taken for iterative: " + ((System.nanoTime - start) / 1000000000.0));
      }
    } else {
      println("Invalid entry.");
    }
  }
}
