class Solution:
    def trap(self, height: List[int]) -> int:
        leftm=[]
        rightm=[]
        lm,rm=0,0
        water=0
        for i in range(len(height)):
            leftm.append(lm)
            lm=max(lm,height[i])
        for j in range(len(height)-1,-1,-1):
            rightm.append(rm)
            rm=max(rm,height[j])
        rightm.reverse()
        for k in range(len(height)):
            temp=0
            temp=((min(leftm[k],rightm[k]))-height[k])
            if temp>0:
                water+=temp
        return water

        

