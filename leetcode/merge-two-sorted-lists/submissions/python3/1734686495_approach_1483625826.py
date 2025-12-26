# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy=ListNode(-1)
        curr=dummy
        temp1=list1
        temp2=list2
        while temp1 and temp2:
            if temp1.val<=temp2.val:
                curr.next=temp1
                temp1=temp1.next
            else:
                curr.next=temp2
                temp2=temp2.next
            curr=curr.next
        if temp1:
            curr.next=temp1
        elif temp2:
            curr.next=temp2
        return dummy.next


        