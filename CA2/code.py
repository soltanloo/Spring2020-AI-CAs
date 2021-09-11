import re
import string
import random
import copy
from nltk.tokenize import word_tokenize
ALPHABET = "abcdefghijklmnopqrstuvwxyz"
MAX_GENERATIONS = 5000
ELITES_SIZE = 50
INITIAL_POPULATION = 1000
GENERATION_SIZE = 500
MAX_REPETITIONS = 5

class Decoder:
  def __init__(self, cipher_text):
    self.cipher_text = cipher_text

  def decode(self):
    return self.genetic_algorithm(self.cipher_text)

  def read_file(self, file_path):
    with open(file_path, 'r') as myfile:
      return myfile.read()
      
  def clean_text(self, text):
    new_text = text.lower()
    new_text = re.sub(r"\d+", " ", new_text)
    for ch in string.punctuation:                                                                                                     
      new_text = new_text.replace(ch, " ")
    new_text = ' '.join(new_text.split())
    word_tokens = word_tokenize(new_text) 
    data = new_text.split()
    return set(word_tokens)

  def create_dict_key(self, key_string):
    dict_key = dict()
    for i in range(len(ALPHABET)):
      dict_key[ALPHABET[i]] = key_string[i]
    return dict_key

  def create_empty_dict(self):
    return {chr(i):'' for i in range(97, 123)}

  def decrypt(self, cipher_text, key_dict):
      decrypted_text = ""
      for letter in cipher_text:
          uppercase = letter.isupper()
          if uppercase:
              decrypted_text += key_dict[letter.lower()].upper()
          else:
              if letter in ALPHABET:
                  decrypted_text += key_dict[letter]
              else:
                  decrypted_text += letter

      return decrypted_text

  def calculate_fitness(self, decrypted_text, dictionary):
      fitness = 0
      for word in decrypted_text:
          if word in dictionary or word in ALPHABET:
              fitness += 1
      return fitness

  def crossover(self, parent_key1, parent_key2, shock = False):
      parent_key1 = self.create_dict_key(parent_key1)
      parent_key2 = self.create_dict_key(parent_key2)

      slice_index = random.randrange(0, 26)
      child1 = self.merge_parents(parent_key1,parent_key2,slice_index)
      child2 = self.merge_parents(parent_key2,parent_key1,slice_index)

      is_mutated = random.randrange(0, 10)
      if is_mutated < 7 or shock:
          child1 = self.mutate_child(''.join(child1), shock)
          child2 = self.mutate_child(''.join(child2), shock)

      child1 = ''.join(child1)
      child2 = ''.join(child2)
      return [child1, child2]

  def merge_parents(self, parent_key1, parent_key2, slice_index):
      child = self.create_empty_dict()
      
      for i in range(0, slice_index):
          current_letter = chr(i + 97)
          child[current_letter] = parent_key1[current_letter]

      for j in range(slice_index, len(parent_key2)):
          current_letter = chr(j + 97)
          if parent_key2[current_letter] not in child.values() and child[current_letter] == '':
              child[current_letter] = parent_key2[current_letter]

      shuffled_alhpabet = copy.deepcopy(list(ALPHABET))
      random.shuffle(shuffled_alhpabet)
      for a in shuffled_alhpabet:
          for k in child:
              if a not in child.values() and child[k] == '':
                  child[k] = a
                  
      child = list(child.values())
      return child

  def mutate_child(self, original, shock):
      mutated_child = self.create_dict_key(original)
      if shock:
          mutations = random.randint(10,20)
      else:
          mutations = random.randint(1,5)
      for i in range(0, mutations):
          idx1 = random.randint(0,25)
          idx2 = random.randint(idx1,25)
          temp = mutated_child[chr(idx1 + 97)]
          mutated_child[chr(idx1 + 97)] = mutated_child[chr(idx2 + 97)]
          mutated_child[chr(idx2 + 97)] = temp    
      return list(mutated_child.values())

  def sort_dict(self, dictionary):
      sorted_dict_list = sorted(copy.deepcopy(dictionary), key=dictionary.get, reverse=True)
      return sorted_dict_list

  def genetic_algorithm(self, cipher_text):
      cleaned_data = self.clean_text(self.read_file('global_text.txt'))
      gen_num = 0
      hold_text = {}
      parents = [''.join(random.sample(ALPHABET, len(ALPHABET))) for i in range(INITIAL_POPULATION)]
      last_top_fitness = 0
      repeated_fitness = 0

      while gen_num < MAX_GENERATIONS:
          decryptions = {}
          for parent in parents:
              parent_key = self.create_dict_key(copy.deepcopy(parent))
              decrypted_text = self.decrypt(cipher_text, parent_key)
              cleaned_decrypted_text = self.clean_text(decrypted_text)
              fitness = self.calculate_fitness(cleaned_decrypted_text, cleaned_data)
              decryptions[parent] = fitness
              hold_text[parent] = decrypted_text
              if fitness == len(cleaned_decrypted_text):
                  return hold_text[parent]

          parents_sorted = self.sort_dict(copy.deepcopy(decryptions))
          if last_top_fitness == decryptions[parents_sorted[0]]:
              repeated_fitness += 1
          else:
              repeated_fitness = 0
              last_top_fitness = decryptions[parents_sorted[0]]
          
          new_generation = []

          for i in range(0, ELITES_SIZE):
              for j in range(0, 4):
                  parent1 = parents_sorted[i]
                  parent2 = parents_sorted[i+1]
                  chance = random.randint(0, 9)
                  if chance > 3:
                      new_generation += self.crossover(parent1, parent2)

          parents = parents_sorted[0:ELITES_SIZE] + new_generation[:GENERATION_SIZE - ELITES_SIZE]
          
          if repeated_fitness >= MAX_REPETITIONS:
              if repeated_fitness % MAX_REPETITIONS == 0:
                  for i in range(0, GENERATION_SIZE):
                      idx1 = random.randint(0, ELITES_SIZE - 1)
                      idx2 = random.randint(0, ELITES_SIZE - 1)
                      parent1 = parents_sorted[idx1]
                      parent2 = parents_sorted[idx2]
                      parents += self.crossover(parent1, parent2)

          gen_num += 1


encoded_text = open("encoded_text.txt").read()
d = Decoder(encoded_text)
decoded_text = d.decode()
print(decoded_text)
