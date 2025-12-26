class Solution:
    def maxChunksToSorted(self, arr: List[int]) -> int:
        rs=0
        i_sum=0
        cnt=0
        for i in range(len(arr)):
            rs+=arr[i]
            i_sum=(i*(i+1))//2
            if rs==i_sum:
                cnt+=1
        return cnt


        
        