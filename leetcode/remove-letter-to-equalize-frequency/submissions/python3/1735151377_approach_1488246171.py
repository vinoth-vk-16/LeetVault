class Solution:
    def equalFrequency(self, word: str) -> bool:
        a=Counter(word)
        for char in list(a):
            a[char]-=1
            if a[char]==0:
                del a[char]
            if len(set(a.values()))==1:
                return True
            a[char]+=1
        return False
                
        