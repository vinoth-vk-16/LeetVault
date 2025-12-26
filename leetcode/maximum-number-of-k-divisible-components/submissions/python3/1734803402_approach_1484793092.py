from typing import List, Dict

class Solution:
    def maxKDivisibleComponents(self, n: int, edges: List[List[int]], values: List[int], k: int) -> int:
        # Build the tree using an adjacency list
        tree: Dict[int, List[int]] = {i: [] for i in range(n)}
        for a, b in edges:
            tree[a].append(b)
            tree[b].append(a)
        
        # To store the number of components
        components = 0

        # DFS function to calculate the sum modulo k for each subtree
        def dfs(node: int, parent: int) -> int:
            nonlocal components
            subtree_sum = values[node]

            # Traverse all neighbors except the parent
            for neighbor in tree[node]:
                if neighbor != parent:
                    subtree_sum += dfs(neighbor, node)

            # If the subtree sum modulo k is zero, it forms a valid component
            if subtree_sum % k == 0:
                components += 1
                return 0  # This component is removed from its parent
            
            return subtree_sum % k  # Return the remaining value

        # Start DFS from node 0 (or any node)
        dfs(0, -1)

        return components
