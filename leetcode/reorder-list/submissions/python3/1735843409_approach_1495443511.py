# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if not head:
            return 
        st=[]
        stt=head
        while stt:
            st.append(stt)
            stt=stt.next
        temp=head
        for _ in range(len(st)//2):
            nn=st.pop()
            nextn=temp.next
            temp.next=nn
            nn.next=nextn
            temp=nextn
        temp.next=None
        

        