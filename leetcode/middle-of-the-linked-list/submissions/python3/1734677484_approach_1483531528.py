# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        temp=head
        cnt=0
        while temp:
            cnt+=1
            temp=temp.next
        cnt1=0
        st=[]
        temp1=head
        while temp1:
            if cnt1>=(cnt//2):
                head=temp1
                return head
            temp1=temp1.next
            cnt1+=1
        