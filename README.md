# debruijn-graph-implementation
Debruijn Graphs for k-universal-string (circularity enforced)

Ensure that you have following modules installed:
- matplotlib
- networkx

# overlap graph

! overlapGraph is overlaped graphs selected using a greedy heuristic of maximum cycle overlap. (heuristic => not the exact DNA is composed) (problem is NP-Hard using overlap technique - Hamiltonian Cycle)
! current problem being that we need roughly x20 times the total DNA strand size (segmented in 20% per read). Need to experiment with other ratios and note observations ( keeping in mind conventional tradeoffs)
