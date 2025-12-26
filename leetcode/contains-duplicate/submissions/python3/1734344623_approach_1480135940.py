class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        st=set()
        for val in nums:
            if val in st:
                return True
            st.add(val)
        return False
        