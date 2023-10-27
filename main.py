from typing import List
import random
import math
import time
import ast


def convert_text(_string: str) -> List[int]:
    # Takes a string and converts into a list of integers using ord(), each item in list representing the ASCII number
    # of every character in string
    integer_list = []
    for ch in _string:
        integer_list.append(ord(ch))
    return integer_list


def convert_num(_list: List[int]) -> str:
    # Takes list of ints and using chr() converts each int to its equivalent ASCII character and adds to empty string
    _string = ''
    for i in _list:
        _string += chr(i)
    return _string


def convert_binary_string(_int: int) -> str:
    # Converts decimal number to its binary expansion using modulus 2 operation and division by 2
    bin_list = []
    remainder = 0

    # Loop through tracking modulus of _int value & adding to bin_list & updating _int through integer division
    # by 2 each time
    while _int > 0:
        remainder = _int % 2
        _int = _int // 2
        bin_list.append(str(remainder))

    # Reverse list so that binary values are rearranged going most significant digits to least significant (l to r)
    bin_list = bin_list[::-1]
    bits = ''.join(bin_list)
    return bits


def fme(b: int, n: int, m: int) -> int:
    # Takes integers b, n, m as inputs, reduces b^n into its binary expansion, and calculates the modulus with respect
    # to m by applying distributive property of modular multiplication
    remainder = 1
    power = b % m
    bin_n = convert_binary_string(n)  # Convert exponent to binary string

    # Modify binary str into int list and reverse (to go from least significant digit to most significant)
    list_bin_n = [int(digit) for digit in bin_n]
    list_bin_n = list_bin_n[::-1]

    # Loop through binary digits and if digit is 1, remainder is updated; power is updated to provide remainder at
    # (b^2)^j where j = i + 1; i being the location of each digit in bin number
    bin_n_len = len(list_bin_n)

    for i in range(bin_n_len):
        if list_bin_n[i] == 1:
            remainder = (remainder * power) % m
        power = (power * power) % m
    return remainder


def euclidean_alg(a: int, b: int) -> int:  # Calculates the greatest common divisor of inputs a & b
    # Checks to see if a >= b or if b >= a and divides larger value by smaller value updating remainder until remainder
    # equals 0 and returns updated divisor
    if a >= b >= 0:
        while b > 0:
            k = a % b
            a = b
            b = k
        return a
    elif b >= a >= 0:
        while a > 0:
            k = b % a
            b = a
            a = k
        return b
    else:
        return "Enter positive integers as parameters"


def ext_euclidean_alg(a: int, b: int) -> tuple[int, int, int]:
    # Set initial values for s1, t1, s2, t2 so that coefficients can be checked
    s1, t1 = 1, 0
    s2, t2 = 0, 1
    # Set a_ as the largest of a, b and b_ as smallest
    a_, b_ = max(a, b), min(a, b)

    while b_ > 0:
        # Calculates remainder and quotient k, q
        k = a_ % b_
        q = a_ // b_
        # Update new value of a to b and new b to remainder (k)
        a_ = b_
        b_ = k
        # Use s1_hat, t1_hat, s2_hat, t2_hat to temporarily store new values for s1, t1, s2, t2
        s1_hat, t1_hat = s2, t2,
        s2_hat, t2_hat = s1 - q * s2, t1 - q * t2
        s1, t1 = s1_hat, t1_hat
        s2, t2, = s2_hat, t2_hat

    # Adjust s, t based on which of a and b was larger int value
    if a > b:
        return a_, s1, t1
    elif b > a:
        return a_, t1, s1


def find_public_key_e(p: int, q: int) -> tuple[int, int]:
    # Calculate n (public key) as product of two primes, phi(n) as number of co-primes that exist for n
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = phi_n - 1
    potential_e = []

    # Loop thru values of e starting with phi_n - 1, checking to see if phi_n and e are relatively prime.
    # If relatively prime, add to list of potential_e
    while e > 1 and len(potential_e) <= 1000000:
        if euclidean_alg(phi_n, e) == 1:
            potential_e.append(e)
        e -= 1

    # From list of potential candidates of e, randomly select an int as the index value of list
    rand_i = random.randint(0, len(potential_e))
    e = int(potential_e[rand_i])

    return e, n


def find_private_key_d(e: int, p: int, q: int) -> int:
    phi_n = (p - 1) * (q - 1)  # Calculate Phi(n) to be the number of co-primes that n (= p*q) has
    *_, d = ext_euclidean_alg(phi_n, e)  # Calculate Bezout coefficients using EEA, with d equal to the t1 value

    # If the d value is negative, keep adding phi_n (the modulo number) until d is positive.
    while d < 0:
        d += phi_n
    return d


def encode(n: int, e: int, message: str) -> List[int]:
    cipher_text = []
    msg_int = convert_text(message)  # Convert message input to ASCII int list

    # Apply fme to each int value in list to encode
    for num in msg_int:
        cipher_text.append(fme(num, e, n))
    return cipher_text


def decode(n: int, d: int, cipher_text: List[int]) -> str:
    message = ''
    msg_list = []

    # Apply fme to each int value to encoded input msg to decode
    for num in cipher_text:
        msg_list.append(fme(num, d, n))

    # Convert decoded numbers to ASCII characters & return as string
    message = convert_num(msg_list)
    return message


def pseudo_random_gen(x: int, n: int) -> int:
    return (x ** 2 + 1) % n


def pollards_rho(n: int) -> str:
    if n > 1:
        start_time = time.time()
        a = 2
        b = a
        p = 1

        while p == 1:
            a = pseudo_random_gen(a, n)
            b = pseudo_random_gen(pseudo_random_gen(b, n), n)
            p = euclidean_alg(abs(a - b), n)
        end_time = time.time()
        if p == n:
            print(end_time - start_time)
            return 'failure - n is a prime'
        else:
            print("Time for Pollard's Rho Algorithm Factorization: {}".format(end_time - start_time))
            return p
    else:
        return 'n must be int greater than 1'


def main():
    while True:
        val = input("""
                 ~~~ RSA ~~~
        Select from the Following Options:
        1. Create Public Keys
        2. Encode a Message
        3. Decode a Message
        4. Exit
        """)

        if val == '1':
            p1 = int(input("Enter a prime number: "))
            q1 = int(input("Enter a different prime number: "))

            e1, n1 = find_public_key_e(p1, q1)

            print("""Your public keys are: 
                     n: {} 
                     e: {}""".format(n1, e1))

        elif val == '2':
            n2 = int(input("Enter n from public key: "))
            e2 = int(input("Enter e from public key: "))

            encode_msg = input("Enter message to encode: ")
            encoded_cipher = encode(n2, e2, encode_msg)

            print("""Your encoded message is: {}
            """.format(encoded_cipher))

        elif val == '3':
            n3 = int(input("Enter n from public key: "))
            e3 = int(input("Enter e from public key: "))
            decode_msg = input("Enter message to decode: ")

            new_decode_msg = ast.literal_eval(decode_msg)
            new_decode_msg = [num for num in new_decode_msg]

            p3 = pollards_rho(n3)
            q3 = int(n3 / p3)
            d3 = find_private_key_d(e3, p3, q3)

            decipher_txt = decode(n3, d3, new_decode_msg)

            print("""Your deciphered message is: {}
            """.format(decipher_txt))

        elif val == '4':
            return


if __name__ == '__main__':
    main()