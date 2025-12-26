class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        mp=defaultdict(list)
        for val in strs:
            sort_v=''.join(sorted(val))
            mp[sort_v].append(val)
        return list(mp.values())

        