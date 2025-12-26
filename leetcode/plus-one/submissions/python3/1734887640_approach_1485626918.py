class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        la=0
        arr=[]
        for val in digits:
            la+=val
            la*=10
        la=(la//10)+1
        la=str(la)
        for val in la:
            arr.append(int(val))
        return arr
        
