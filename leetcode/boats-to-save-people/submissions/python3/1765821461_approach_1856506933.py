class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        l,r=0,len(people)-1
        cnt=0
        while l<r:
            if people[l]+people[r]<=limit:
                l+=1
                r-=1
            else:
                if people[l]>people[r]:
                    
                    l+=1
                else:
                    r-=1
            cnt+=1
        if l==r:
            cnt+=1
        return cnt



        