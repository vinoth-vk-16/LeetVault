class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        pref=strs[0]
        for val in strs:
            while not val.startswith(pref):
                pref=pref[:-1]
                if not pref:
                    return ""
        return pref
        
                
                

            
