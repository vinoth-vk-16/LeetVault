class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []  # Return an empty list if no digits are provided
        
        ph = {
            '2': ("a", "b", "c"),
            '3': ("d", "e", "f"),
            '4': ("g", "h", "i"),
            '5': ("j", "k", "l"),
            '6': ("m", "n", "o"),
            '7': ("p", "q", "r", "s"),
            '8': ("t", "u", "v"),
            '9': ("w", "x", "y", "z")
        }
        
        # Build the array of letters corresponding to each digit
        arr = [list(ph[val]) for val in digits]
        print(arr)
        # Generate the combinations using Cartesian product
        combinations = [''.join(combo) for combo in product(*arr)]
        
        return combinations
