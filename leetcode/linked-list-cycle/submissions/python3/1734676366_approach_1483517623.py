# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        dt={}
        temp=head
        cnt=0
        while temp:
            if temp in dt:
                return True
            else:
                dt[temp]=cnt
            temp=temp.next
        return False
        