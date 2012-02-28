-- From `Learn you Haskell for Great Good!`
-- Types and Typeclasses
-- Fred Song, types.hs

-- '::' operater means "has type of"
-- ex. "1==5 :: Bool"
-- Type starting with capital = Explicit types
-- Type starting with lowercase = type variable (like generics)


-- Explicitly declare input/output of function
{-removeLowercase :: [Char] -> [Char]-}
removeLowercase :: String -> String
removeLowercase str = [c | c <- str, c `elem` ['A'..'Z']]

-- use -> for multi parameters as well
addThree :: Int -> Int -> Int -> Int
addThree a b c = a + b + c

-- Int vs. Integer
factorial :: Integer -> Integer
factorial n = product [1..n]

---------------------
-- Typeclasses
---------------------
-- `:t (==)` 
-- (==) :: Eq a => a -> a -> bool
-- The == function takes any 2 values of type Eq and returns a Bool

-- `:t elem` 
-- elem :: Eq a => a -> [a] -> bool
-- `elem` takes a Eq value and a list of Eq elements, returns a Bool

-- Eq: types supporting equality testing
-- Ord: types that have an ordering (ex. used with < and >)
-- Enum: can be enumerated (i.e using succ)
-- Show: can be presented as strings
-- Read: can be converted from string to another type
