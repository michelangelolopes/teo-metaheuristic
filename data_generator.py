import random

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)

def set_data(data_file, sequences_set):
    data_file = open(data_file, "w")

    for i in sequences_set:
        data_file.writelines(i + "\n")
    
    data_file.close()

alphabet = list(char_range('a', 'e'))
max_sequence_length = 20
min_sequence_length = 5
qtd_sequences = 100
sequences_set = []
print(alphabet)

for i in range(0, qtd_sequences):
    sequence_length = random.randint(min_sequence_length, max_sequence_length - 1)
    print(sequence_length)
    sequence = ""
    
    for j in range(0, sequence_length):
        letter = random.randint(0, len(alphabet) - 1)
        sequence += alphabet[letter]

    sequences_set.append(sequence)

print(sequences_set)
set_data("scs_problem_samples.txt", sequences_set)