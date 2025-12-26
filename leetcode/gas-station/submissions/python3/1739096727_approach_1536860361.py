class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        tg,tc=0,0
        tank,start=0,0
        for i in range(len(gas)):
            tg+=gas[i]
            tc+=cost[i]
            tank+=(gas[i]-cost[i])

            if tank<0:
                start=i+1
                tank=0
        return start if tg>=tc else -1

        