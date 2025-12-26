# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []
        res=[]
        def trav(root):
            if root.left is not None:
                trav(root.left)
            res.append(root.val)
            if root.right is not None:
                trav(root.right)
            return res
        trav(root)
        return res