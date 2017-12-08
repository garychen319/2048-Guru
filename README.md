2048 Game + Solver AI

To run: From folder starter, python3 GameManager_3.py

The hi-score results between implementing just minimax and minimax with alpha beta pruning did not make a significant observable difference, however does decerease run time. Ran 5 tests with mimimax and 5 tests with mimimax + alpha beta pruning, and the average of the tests was ~200 lower, but may have just been because of outlier results that ended the game early. Pruning helps by reducing the run time so the search can run to a greater depth than without pruning in the alloted time.

