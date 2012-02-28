-- From `Learn you Haskell for Great Good!`
-- Syntax in Functions
-- Fred Song, types.hs

----------------------------
-- Misc
----------------------------
-- Seperate bodies can be defined for functions based on input
lucky :: (Integral a) => a -> String
lucky 7 = "LUCKY NUMBA 7!!"
lucky x = "No lucky buddy"

-- We can do recursion in Haskell as well (duh...)
-- A seperate body for the base case removes the need for an ugly if 
factorial :: (Integral a) => a -> a
factorial 0 = 1
factorial n = n * factorial (n-1)

-- We can 'split' parameters when declaring them
addVectors :: (Num a) => (a,a) -> (a,a) -> (a,a)
-- addVector x y = (fst x + fst y, snd x + snd y)
addVectors (a,b) (c,d) = (a+c, b+d)

-- Extending fst and snd to 3-tuples
first :: (a,b,c) -> a
second :: (a,b,c) -> b
third :: (a,b,c) -> c

first (a,_,_) = a
second (_,b,_) = b
third (_,_,c) = c

----------------------------
-- Pattern Matching
----------------------------
-- (x:xs) in the parameters is a common
-- x is first element in list and xs is the rest
head':: [a] -> a
head' [] = error "Can't call head on empty list"
head' (x:xs) = x

-- more param pattern matching examples
tell :: Show a => [a] -> String
tell [] = "List empty"
tell (x:[]) = "List has 1 element: " ++ show x
tell (x:y:[]) = "List has 2 element: " ++ show x ++ " and " ++ show y
tell (x:y:_) = "List too long, here's first 2 elements " ++ show x ++ " and " ++ show y

length' :: [a] -> Int
length' [] = 0
length' (_:xs) = 1 + length' xs

sum' :: Num a => [a] -> a
sum' [] = 0
sum' (x:xs) = x + sum' xs

-- '@' operator allows easy access to entire pattern
capital :: String -> String
capital "" = "Empty String"
capital all@(x:xs) = "The first letter of " ++ all ++ " is " ++ [x]

----------------------------
-- Guards
----------------------------
