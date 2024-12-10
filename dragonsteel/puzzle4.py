# def to_base_3(n):
#   """Converts a decimal number to base 3."""
#   if n == 0:
#     return "0"
#   result = ""
#   while n > 0:
#     result = str(n % 3) + result
#     n //= 3
#   return result


# def iterate_options():
#     yield to_base_3(i)


def print_values(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden):
    print('fen', fen, 'gaz', gaz, 'hesina', hesina, 'jasnah', jasnah, 'kaladin', kaladin, 'lopen', lopen, 'mraize', mraize, 'orodon', oroden)
    

def print_chouta(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden):
  chouta = ['chouta']

  if fen == 'chouta':
    chouta.append('fen')

  if gaz == 'chouta':
    chouta.append('gaz')

  if hesina == 'chouta':
    chouta.append('hesina')

  if jasnah == 'chouta':
    chouta.append('jasnah')

  if kaladin == 'chouta':
    chouta.append('kaladin')

  if lopen == 'chouta':
    chouta.append('lopen')

  if mraize == 'chouta':
    chouta.append('mraize')

  if oroden == 'chouta':
    chouta.append('oroden')
    
  if len(chouta) == 4 or len(chouta) == 5:
    print(' '.join(chouta))


def print_gaz(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden):
  if gaz == 'chouta':
    print('gaz', end=' ')
    print_values(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden)


def count_haspers(*args):
  return args.count('haspers')


def combos(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden):
  pass


def haspers_pairs(values, fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden):
  if 'fen and gaz' in values and fen == gaz and fen == 'chouta':
    values.remove('fen and gaz')
  
  if 'fen and lopen' in values and fen == lopen and fen == 'chouta':
    values.remove('fen and lopen')
  
  if 'hesina and oroden' in values and hesina == oroden and hesina == 'chouta':
    values.remove('hesina and oroden')
  
  if 'jasnah and mraize' in values and jasnah == mraize and jasnah == 'chouta':
    values.remove('jasnah and mraize')
    
  if 'kaladin and mraize' in values and kaladin == mraize and kaladin == 'chouta':
    values.remove('kaladin and mraize')
    
  return values


def get_possibilities():
  min_haspers = 8
  pairs = ['fen and gaz', 'fen and lopen', 'hesina and oroden', 'jasnah and mraize', 'kaladin and mraize']
  fen_count = 0

  for i in range(255):
    binary = bin(i)[2:].zfill(8)
    fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden = ['chouta' if val == '0' else 'haspers' for val in list(binary)]

    if fen == 'chouta' and (hesina != 'chouta' or jasnah != 'chouta'):
      continue
    
    if oroden == 'haspers' and gaz != 'haspers':
      continue
    
    if jasnah == 'chouta' and lopen == 'chouta' and mraize == 'chouta':
      continue

    if oroden != 'haspers' and (lopen == 'haspers' or mraize == 'haspers'):
      continue

    # print_chouta(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden)
    # print_gaz(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden)
    
    
    
    haspers = count_haspers(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden)
    if haspers < min_haspers:
      min_haspers = haspers
      
    if fen == 'chouta':
      fen_count += 1
      
    pairs = haspers_pairs(pairs, fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden)

    # print_values(fen, gaz, hesina, jasnah, kaladin, lopen, mraize, oroden)

  print('min haspers', min_haspers)
  print('haspers pairs', ', '.join(pairs))
  print('fen count', fen_count)

get_possibilities()