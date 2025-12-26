class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        pre=strs[0]
        for st in strs:
            while not st.startswith(pre):
                pre=pre[:-1]
                if not pre:
                    return ""
        return pre
        
                
                

            
