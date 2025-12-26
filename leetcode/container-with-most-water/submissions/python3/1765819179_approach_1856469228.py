class Solution:
    def maxArea(self, heights: List[int]) -> int:
        maxi=float('-inf')
        l,r=0,len(heights)-1
        while l<r:
            s=min(heights[l],heights[r])
            maxi=max(maxi,s*(r-l))
            if heights[l]<heights[r]:
                l+=1
            else:
                r-=1
        return maxi