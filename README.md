Advanced Software Engineering Homework 1
Gary Chen gc2676
Sample repo created using previous code




2048 Solver - Artificial Intelligence
Gary Chen
gc2676

To run: From folder starter, python3 GameManager_3.py

The results between implementing just minimax and minimax with alpha beta pruning did not make a significant observable difference. I ran 5 tests with mimimax and 5 tests with mimimax + alpha beta pruning, and the average of the tests was ~200 lower, but that may have just been because one of the tests for minimax tests got 1024 instead of 2048 and pulled down the average. Pruning should help by reducing the run time so the search can run to a greater depth than without pruning in the alloted time.

This assignment was done on python 3.

