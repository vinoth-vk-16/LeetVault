class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        mp={}
        for val in strs:
            sv=''.join(sorted(val))
            if sv not in mp:
                mp[sv]=[val]
            else:
                mp[sv].append(val)
        return (list(mp.values()))
        