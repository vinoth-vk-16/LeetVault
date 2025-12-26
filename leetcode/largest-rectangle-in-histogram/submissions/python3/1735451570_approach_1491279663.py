class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        st=[]
        maxi=0
        for i,h in enumerate(heights):
            start=i
            while st and st[-1][1]>h:
                index,ht=st.pop()
                maxi=max(maxi,ht*(i-index))
                start=index 
            st.append((start,h))
        
        for i,h in st:
            maxi=max(maxi,h*(len(heights)-i))
        return maxi
        