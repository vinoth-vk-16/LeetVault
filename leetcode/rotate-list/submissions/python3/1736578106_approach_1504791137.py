# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None:
            return 
        if head.next is None or k==0:
            return head
        cnt=0
        temp=head
        while temp:
            cnt+=1
            temp=temp.next
        if k%cnt==0:
            return head
        r=k%cnt
        pos=cnt-r
        pos1=0
        temp1=head
        while temp1.next:
            pos1+=1
            if pos1==pos:
                ls=temp1.next
                temp1.next=None
                temp2=ls
                while temp2.next:
                    temp2=temp2.next
                temp2.next=head
                head=ls
                return head
                break
            temp1=temp1.next
        
        
                
        