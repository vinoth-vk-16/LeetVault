class Solution:
    def minimumBoxes(self, apple: List[int], capacity: List[int]) -> int:
        capacity.sort(reverse=True)
        su=sum(apple)
        box=0
        for val in capacity:
            box+=1
            if val>=su:
                break        
            else:
                su=su-val
        return box
            

        