#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Snabb lösning för FRA fjärde advent challenge 2021."""
#
# Möjlig lösning från manuell kontroll:
# öken
# utan
# viga
# tarm
# skal

import itertools
import os
import re
import subprocess

c1c = ["s", "t", "u", "v", "ö"]
c2c = ["i", "k", "t", "k", "a"]
c3c = ["e", "r", "g", "a", "a"]
c4c = ["n", "m", "l", "a", "n"]
filename = "lista.txt"

def generate_word_list(c1l, c2l, c3l, c4l):
    """Generate word list."""
    wlist = []
    for first in c1l:
        for second in c2l:
            for third in c3l:
                for fourth in c4l:
                    current = f"{first}{second}{third}{fourth}"
                    wlist.append(current)
    return wlist

def save_words(word_file, wlist):
    """Save words."""
    with open(word_file, "w", encoding='utf-8') as file:
        for current in wlist:
            file.write(current)
            file.write('\n')

def check_wrong_words(word_file):
    """Check words in file."""
    with subprocess.Popen(["cat", word_file], stdout=subprocess.PIPE, text=True) as cat_process:
        with subprocess.Popen(["aspell", "-d", "sv", "list"], \
                stdin=cat_process.stdout, stdout=subprocess.PIPE, text=True) as aspell_process:
            wrong = aspell_process.stdout.read()
    wrong_list = str(wrong).split('\n')
    wrong_list.remove('')
    return wrong_list

def words_starts_char(character, wlist):
    """Select words in starting with char in wlist."""
    char_words = []
    for current in wlist:
        check_char = re.compile("^" + character)
        if check_char.search(current):
            char_words.append(current)
    return char_words

# Skapa lista av möjliga ord
combinations = list(set(generate_word_list(c1c, c2c, c3c, c4c)))
# Spara till fil
save_words(filename, combinations)
# Vilka kombinationer är inte ord
wrong_words = check_wrong_words(filename)
os.unlink(filename)
# Ta bort felaktiga ord
for wrong_word in wrong_words:
    combinations.remove(wrong_word)

# Gör en list av ord per bokstav
word_list = []
for char in c1c:
    word_list.append(words_starts_char(char, combinations))

# Slå ihop de olika orden till alla alternativ
solutions = []
for solution in list(itertools.product(*word_list)):
    solutions.append(" ".join(solution))

# Sortera de ursprungliga listorna
c1c.sort()
c2c.sort()
c3c.sort()
c4c.sort()

# Testa varje lösning från solutions.
# Skriv ut korrekta lösningar.
for row in list(set(solutions)):
    st1 = []
    st2 = []
    st3 = []
    st4 = []
    words = row.split(" ")
    complete = True
    for word in words:
        st1.append(word[0])
        st2.append(word[1])
        st3.append(word[2])
        st4.append(word[3])
    st1.sort()
    st2.sort()
    st3.sort()
    st4.sort()
    if st1 == c1c and st2 == c2c and \
        st3 == c3c and st4 == c4c:
        print(row)
