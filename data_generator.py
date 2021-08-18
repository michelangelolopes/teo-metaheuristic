import random

def char_range(char_1, char_2): #gera um range de caracteres, de char_1 a char_2 (inclusive)
    for char_code in range(ord(char_1), ord(char_2) + 1):
        yield chr(char_code)

def set_data(data_file, sequences_list): #escreve uma lista de sequências geradas em um arquivo .txt
    data_file = open(data_file, "w")

    for i in sequences_list:
        data_file.writelines(i + "\n")
    
    data_file.close()

def get_data(data_file): #pega as sequências de um arquivo .txt e armazena em uma lista
    data_file = open(data_file, "r")
    sequences_list = data_file.readlines()

    for i in range(0, len(sequences_list)):
        sequences_list[i] = sequences_list[i].replace("\n", "")

    data_file.close()
    return sequences_list

if __name__ == "__main__":
    alphabet = list(char_range('a', 'z'))
    max_sequence_length = 100
    min_sequence_length = len(alphabet)
    qtd_sequences = 1000
    sequences_list = []
    #print(alphabet)

    for i in range(0, qtd_sequences):
        sequence_length = random.randint(min_sequence_length, max_sequence_length - 1)
        print(sequence_length)
        sequence = ""
        
        for j in range(0, sequence_length):
            letter = random.randint(0, len(alphabet) - 1)
            sequence += alphabet[letter]

        sequences_list.append(sequence)

    print(sequences_list)
    set_data("samples.txt", sequences_list)