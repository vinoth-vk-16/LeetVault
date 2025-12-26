class Solution:
    def maxArea(self, height: List[int]) -> int:
        n=len(height)
        left=0
        right=n-1
        max1=0
        while left<right:
            area = min(height[left], height[right]) * (right - left)
            max1=max(area,max1)
            if height[left]<height[right]:
                left+=1
            else:
                right-=1
        return max1
        


            
        
        