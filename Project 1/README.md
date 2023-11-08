# Project 1 : Search

This folder contains the files for Project 1: Search. The solutions files you should be looking for are: search.py and searchAgents.py.

# Notes

<!-- add a bullet list -->
* search.py contains the solutions for the first 4 questions and searchAgents.py for the remaining 4.
* In questions 1 through 4, I have gone a different route for finding the constructed path that you may have seen others have taken. I use a dictionary called `connections` that stores `(Current State : (Previous State, Direction from Previous to Current State))` pairs. This allows me to construct the path by backtracking from the goal state to the start state. Many other solutions just construct the path as they go along which is both space inefficient and less elegant.
* Traditionally, I have used a visited set to keep track of explored nodes in the DFS and BFS algorithms. However, on the UCS and A* algorithms, I switched the set for a second additional dictionary called `costs` that is used to keep track both of the explored nodes and the currently cheapest cost to get to that node. This allows me to avoid having to check if a node is in the fringe and then checking if the cost to get to that node is cheaper than the current cost.
* To find all the corners in question 6, I have used a heuristic that prioritizes states based on their Manhattan distance from the furthest alive corner. One can show with a bit of math that the heuristic is both admissible and consistent. Even though this heuristic is not the most efficient, it is still good enough to pass the autograder with a perfect score. The best heuristic that I have found upon researching is one that sums the distances from the state to the closest corner and then that corner to the next closest corner and so on.
* Similarly, in question 7, I have used a similar technic by switching the Manhattan distance for the Maze distance between the state and the furthest corner. This heuristic is also admissible and consistent. Even though I haven't tested it, you could again use the "snaking" method described above and it would probably even work with just the Manhattan distance.