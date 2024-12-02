# !/bin/python3

from src.utils import read_input 

def process_input(data):
  list_a = []
  list_b = []

  for line in data:
    a, b = line.split('   ')
    list_a.append(int(a))
    list_b.append(int(b))
    
  return list_a, list_b

def part_a(values_a, values_b):
  sorted_a = sorted(values_a)
  sorted_b = sorted(values_b)
  
  sum = 0
  for a, b in zip(sorted_a, sorted_b):
    sum += abs(a - b)
    
  return sum

def part_b(list_a, list_b):
  sum = 0
  for a in list_a:
    sum += a * list_b.count(a)
    
  return sum

def main():
  list_a, list_b = process_input(read_input())
  print(part_a(list_a, list_b))
  print(part_b(list_a, list_b))

main()