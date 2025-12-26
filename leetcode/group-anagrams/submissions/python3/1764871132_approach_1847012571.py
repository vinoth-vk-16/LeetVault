from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        df=defaultdict(list)
        for word in strs:
            key="".join(sorted(word))
            df[key].append(word)
        return list(df.values())
        