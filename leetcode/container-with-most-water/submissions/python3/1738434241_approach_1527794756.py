class Solution:
    def maxArea(self, height: List[int]) -> int:
        left=0
        right=len(height)-1
        m=0
        h=0
        m1=0
        while left < right:
            h=min(height[left],height[right])
            m1=right-left
            m=max(m,(m1*h))
            if height[left]<height[right]:
                left+=1
            else:
                right-=1
        return m

        


            
        
        