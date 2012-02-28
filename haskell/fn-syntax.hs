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
-- <name> <pattern> = <expression>
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
bmiTell :: RealFloat a => a -> a -> String
bmiTell weight height
    | bmi <= skinny = "Underweight"
    | bmi <= normal = "Normal"
    | bmi <= fat = "Lose some weight"
    | otherwise   = "Whale"
    where bmi = weight / height^2 
          (skinny, normal, fat) = (18.5, 25.0, 30.0)

calcBmis :: RealFloat a => [(a,a)] -> [a]
calcBmis bmis = [bmi w h | (w,h) <- bmis]
    where bmi weight height = weight / height^2

-- NOTE: we can define functions using backtick syntax as well!
myCompare :: Ord a => a -> a -> Ordering
a `myCompare` b
    | a > b     = GT
    | a == b    = EQ 
    | otherwise = LT

-- We can use pattern matching in where
initial :: String -> String -> String
{-initial (f:_) (l:_) = [f] ++ "." ++ [l] ++ "."-}
initial first last = [f] ++ "." ++ [l] ++ "."
    where (f:_) = first
          (l:_) = last

----------------------------
-- Let Bindings
----------------------------
-- let <bindings> in <expressions>
cylinder :: RealFloat a => a -> a -> a
cylinder r h = 
    let sideArea = 2*pi*r
        topArea = pi*r^2
    in  sideArea + 2*topArea

-- let vs. where:
-- let is expression like if; where is syntactic construct
{-4 * (let a = 9 in a + 1 ) + 2-}
{-let sq x = x*x in (sq 3, sq 4, sq 5)-}
{-(let a=1;b=2;c=3 in a*b*c, let foo="hey ";bar="there" in foo ++ bar)-}

-- Using let expressions in list comprehensions
-- We don't need the `in` for this case
calcBmis' :: RealFloat a => [(a,a)] -> [a]
calcBmis' bmis = [bmi | (w,h) <- bmis, let bmi=w/h^2, bmi>=25.0]


----------------------------
-- Case Expressions
----------------------------
-- case <expression> of (<pattern> -> <expression>)*

describeList :: [a] -> String
describeList xs = "The list is " ++ case xs of []  -> "empty"
                                               [x] -> "a singleton"
                                               xs  -> "a longer list"

-- NOTE: <pattern> is like what's accepted in the function parameters
describeList' :: [a] -> String
describeList' xs = "The List is " ++ what xs
    where what []   = "empty"
          what [x]  = "a singleton"
          what xs   = "a longer list"

