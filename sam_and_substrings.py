# !/usr/bin/python3
# https://www.hackerrank.com/challenges/sam-and-substrings/problem

string = input().strip()
total = 0
for i in range(0, len(string) + 1):
    for j in range(i + 1, len(string) + 1):
        total += int(string[i:j])
print(total % 1000000007)
