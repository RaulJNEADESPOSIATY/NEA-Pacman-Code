boards = [
[6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
[3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 4, 5, 1, 4, 4, 1, 6, 4, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 2, 3, 0, 0, 3, 1, 3, 3, 1, 0, 3, 1, 3, 3, 1, 3, 0, 1, 3, 3, 1, 3, 0, 0, 3, 2, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 8, 1, 4, 8, 1, 7, 8, 1, 7, 4, 1, 7, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 3, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 3, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 3, 0, 0, 3, 1, 3, 6, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 5, 3, 1, 3, 0, 0, 3, 1, 3, 3],
[3, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 3],
[8, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 6, 4, 4, 9, 9, 4, 4, 5, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 7],
[4, 8, 1, 7, 4, 4, 8, 1, 7, 8, 1, 3, 0, 0, 0, 0, 0, 0, 3, 1, 7, 8, 1, 7, 4, 4, 8, 1, 7, 4],
[0, 0, 0, 0, 0, 0, 0, 0.5, 1, 1, 1, 3, 0, 0, 0, 0, 0, 0, 3, 1, 1, 1, 0.5, 0, 0, 0, 0, 0, 0, 0],
[4, 5, 1, 6, 4, 4, 5, 1, 6, 5, 1, 3, 0, 0, 0, 0, 0, 0, 3, 1, 6, 5, 1, 6, 4, 4, 5, 1, 6, 4],
[5, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 6],
[3, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 3],
[3, 3, 1, 3, 0, 0, 3, 1, 3, 3, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 3, 3, 1, 3, 0, 0, 3, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 3, 1, 3, 5, 1, 3, 3, 1, 6, 3, 1, 3, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 3, 1, 3, 8, 1, 7, 8, 1, 7, 3, 1, 3, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3],
[3, 7, 4, 5, 1, 6, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 5, 1, 6, 4, 8, 3],
[3, 6, 4, 8, 1, 3, 3, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 3, 3, 1, 7, 4, 5, 3],
[3, 3, 1, 1, 1, 3, 3, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 3, 3, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 8, 3, 1, 3, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 3, 1, 3, 7, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
[7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]
         ]