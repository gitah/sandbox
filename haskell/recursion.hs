-- From `Learn you Haskell for Great Good!`
-- Recursion
-- Fred Song, recursion.hs

-- No for/while loops in Haskell!!!
-- This means we must use RECURSION
maximum' :: Ord a => [a] -> a
maximum' [] = error "empty"
maximum' [x] = x
maximum' (x:xs)
    | x > maxTail = x
    | otherwise = maxTail
    where maxTail = maximum' xs

-- Clearer way of defining this function
maximum'' :: Ord a => [a] -> a
maximum'' [] = error "empty"
maximum'' [x] = x
maximum'' (x:xs) = max x (maximum'' xs)

------------------------------------------------------
-- Implementing built in list function using recursion
------------------------------------------------------
length' :: [a] -> Int
length' [] = 0
length' (_:xs) = 1 + length' xs

-- Need Ord to use '<=' operation
replicate' :: (Integral i, Ord i) => i -> a -> [a]
replicate' n x 
    | n <= 0 = []
    | otherwise = x:replicate' (n-1) x

take' :: (Num i, Ord i) => i -> [a] -> [a]
take' _ [] = []
take' n (x:xs)
    | n <= 0 = []
    | otherwise = x:take' (n-1) xs

reverse' :: [a] -> [a]
reverse' [] = []
reverse' (x:xs) = reverse' xs ++ [x]

repeat' :: a -> [a]
repeat' x = x:repeat' x

zip' :: [a] -> [b] -> [(a,b)]
zip' [] _ = []
zip' _ [] = []
zip' (x:xs) (y:ys) = (x,y):zip xs ys

elem' :: (Eq a) => a -> [a] -> Bool
elem' _ [] = False
elem' a (x:xs)
    | a == x = True
    | otherwise = a `elem'` xs

-- Poster Child function for Haskell :)
qsort :: (Ord i) => [i] -> [i]
qsort [] = []
qsort (x:xs) = 
    let lt = [n | n <- xs, n <= x]
        gt = [n | n <- xs, n >= x]
    in qsort lt ++ [x] ++ qsort gt
