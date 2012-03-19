-- From `Learn you Haskell for Great Good!`
-- Higher Order Functions
-- Fred Song, high-order-fn.hs

-- The meat of Haskell

------------------------
-- Currying
------------------------
-- Every function in Haskell takes 1 parameter
-- Currying to take more

-- `multThree 3 6 9` is actually `((multThree 3) 6) 9`
multThree :: (Num a) => a -> a -> a -> a
multThree x y z = x*y*z

-- More examples
compareWithHundred :: (Num a, Ord a) => a -> Ordering
compareWithHundred = compare 100

-- We can curry the 2nd parameter in backtick syntax
isUpperAlphanum :: Char -> Bool
isUpperAlphanum = (`elem` ['A'..'Z'])

-- / by default is like `divide`
divideByTen :: Floating a => a -> a
divideByTen = (/10)



-------------------------
-- First class functions
-------------------------
applyTwice :: (a->a) -> a -> a
applyTwice fn x = fn (fn x)

-- Application:
--      applyTwice (multTree 2 3) 6
--      applyTwice (+3) 2
--      applyTwice (3:) [1]

zipWith' :: (a -> b -> c) -> [a] -> [b] -> [c]
zipWith' _ [] _ = []
zipWith' _ _ [] = []
zipWith' fn (x:xs) (y:ys) = (fn x y):(zipWith' fn xs ys)

-- You can do crazy stuff like:
-- zipWith' (zipWith' (*)) [[1,2,3],[3,5,6],[2,3,4]] [[3,2,2],[3,4,5],[5,4,3]]

-- takes fn and returns fn' that calls fn with reversed arguments
flip' :: (a -> b -> c) -> (b -> a -> c)
flip' f = g
    where g x y = f y x

map' :: (a -> b) -> [a] -> [b]
map' _ [] = []
map' fn (x:xs) = fn x : map' fn xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' p (x:xs) 
    | p x = x : filter' p xs
    | otherwise = filter' p xs

-- Note: parameterless function
largestDivisible :: (Integral a) => a
largestDivisible = head (filter p [100000,99999..])
    where p x = x `mod` 3829 == 0
