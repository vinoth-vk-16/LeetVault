class Solution:
    def trap(self, height: List[int]) -> int:
        l,r=0,len(height)-1
        leftm,rightm=height[l],height[r]
        water=0
        while l<r:
            if height[l]<height[r]:
                l+=1
                temp=leftm-height[l]
                if temp>0:
                    water+=temp
                temp=0
            else:
                r-=1
                temp=rightm-height[r]
                if temp>0:
                    water+=temp
                temp=0
            leftm=max(leftm,height[l])
            rightm=max(rightm,height[r])
        return water

                

        

