-- From `Learn you Haskell for Great Good!`
-- Starting out
-- Fred Song, baby.hs



--------------------------------
-- My First Haskell Functions :)
--------------------------------
-- This is a function, parameters are denoted by spaces 
-- <name> [p1 p2 ...] = <expressions>
doubleMe x = x + x

-- Building more complicated function from a smaller one
doubleUs x y = doubleMe x + doubleMe y

-- introducing the 'if expression'
doubleSmallNumber x = if x > 100 then x else x*2
-- `if` is an expression so it must return something
doubleSmallNumber' x = (if x > 100 then x else x*2) + 1

-- Defining a parameterless function
-- Note that functions must be in lowercase
mario = "It's a-me Mario!"

--------------------------------
-- My First Haskell Lists :)
--------------------------------

-- Syntax just like Python lists!
{-lostNumbers = [4,8,15,16,23,42]-}

-- '++' adds to lists
{-[1,2,3,4] ++ [9,10,11,12]-}

-- Strings are lists of chars
{-"wo" ++ "ot"            -}
{-['w','o'] ++ ['o','t'] -- Same as above-}

-- ':' operator (cons) adds to beginning
{-5:[1,2,3,4,5] -}  -- [5,1,2,3,4,5]
{-1:2:3:[]      -}  -- [1,2,3]

-- '!!' operator accesses index of a list
{-"Barack Obama" !! 3 -}  -- 'a'

--------------------------------
-- Haskell List Comprehensions
--------------------------------

-- [<output function> | <ranges>, <predicates>]
{-[x*2 | x <- [1..10], x*2>=12]-}

boomBang xs = [if x < 10 then "BOOM!" else "BANG!" | x <- xs, odd x]
{-boomBang [5..15]-}

nouns = ["hobo","frog","pope"]
adjs = ["lazy","grouchy","scheming"]
{-[a ++ " " ++ n | a<-adjs, n<-nouns]-}

-- '_' means we dont' care about variable
length' xs = sum [1| _ <- xs]

removeLowercase str = [c | c <- str, c `elem` ['A'..'Z']]

-- The infamous 1 line qsort
qsort l = if length l <= 1 then l else qsort [a | a <- l, a < l!!0] ++ [l!!0] ++ qsort [a | a <- l, a > l!!0]

-- Another implementation
qsort' [] = []
qsort' (p:xs) = [x | x<-xs, x<=p] ++ [p] ++ [x | x<-xs, x>=p]


-- Tuples, just like python
triangles = [(a,b,c) | a <- [1..10], b <- [1..10], c <- [1..10], 
               a^2 + b^2 == c^2, a + b + c == 24]

