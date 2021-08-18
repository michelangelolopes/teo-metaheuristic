#import sys
import random
import math
#import data_generator as dg

#exemplo simples, apenas para visualização do retorno de cada heurística de construção
sequences_list = ["aaa", "aab", "abb", "bba", "baa", "bbb"]
#sequences_list = dg.get_data("samples.txt")

def overlay(seq1, seq2): #calcula a quantidade de caracteres que podem ser sobrepostos, do final da sequencia 1 com o começo da sequência 2
    '''
    exemplo: (aaa, aab) -> aa -> count = 2
    '''
    seq1_len = len(seq1) - 1
    if len(seq2) >= len(seq1):
        seq2_len = len(seq1) - 1 #se a seq2 for maior, igualamos o comprimento; se for igual, tanto faz qual comprimento usar
    elif len(seq2) < len(seq1):
        seq2_len = len(seq2) - 1 #se a seq2 for menor, utilizamos o próprio comprimento de seq2

    count = 0
    while count == 0 and seq2_len > -1:
        aux = seq1_len #para não perder o comprimento da seq1 e evitar o calculo de len()

        for i in range(seq2_len, -1, -1):
            if seq1[aux] == seq2[i]: #char igual, incrementa o contador de sobreposição e decrementa o contador de char de seq1
                count += 1
                aux -= 1
            else: #a sobreposição não funcionou, contador é zerado para a próxima iteração
                count = 0
                break
        
        seq2_len -= 1
        
    return count

def common_supersequence(seq1, seq2): #calcula a supersequência comum a duas sequências
    '''
    exemplo: (aaa, aab) -> overlay_count = 2 -> aaa + aab[2:3] -> aaab
    '''
    overlay_count = overlay(seq1, seq2) #calculamos a quantidade de sobreposição possível na sequência
    supersequence = seq1 + seq2[overlay_count:len(seq2)] #retornamos a string que concatena as sequências, desconsiderando os char iniciais da seq2, envolvidos na sobreposição
    return supersequence

def common_supersequence_list(order): #calcula a supersequência comum para sequências em uma lista ordenada
    '''
    exemplo: (aaa, aab, abb) -> (aaab, abb) -> aaabb
    '''
    overlay_seq = sequences_list[order[0]]
    for j in range(1, len(order)):
        overlay_seq = common_supersequence(overlay_seq, sequences_list[order[j]])
    return overlay_seq

#simulated annealing: heurística gulosa para geração de solução inicial
def greedy_algorithm(): #encontra a solução do problema escolhendo as primeiras sequências com maior sobreposição
    seq_list_indexes = list(range(0, len(sequences_list))) #lista com os índices da lista de sequências; com a execução do algoritmo, irá conter também sublistas de índices, para simbolizar sequências sobrepostas

    while len(seq_list_indexes) > 1: #o algoritmo para, quando houver apenas uma sublista de índices
        best_overlay_count = -1
        best_overlay_list_count = []
        seq_list_values = [] #lista com as sequências associadas aos elementos da lista de índices

        for i in seq_list_indexes: #verificamos a lista de índices de seq; ao final, teremos uma lista com as sequências e não seus indíces
            if(isinstance(i, list)): #se o índice for uma sublista de índices, precisamos da supersequência associada a sublista
                seq_list_values.append(common_supersequence_list(i))
            else: #se for apenas um índice, adicionamos a sequência associada ao índice apenas
                seq_list_values.append(sequences_list[i])

        for i in range(0, len(seq_list_values)): #buscamos as sequências com maior sobreposição
            for j in range(0, len(seq_list_values)):
                if(i == j):
                    continue

                overlay_count = overlay(seq_list_values[i], seq_list_values[j])

                if(best_overlay_count < overlay_count): #quando duas sequências tiveram a maior sobreposição da iteração
                    best_overlay_count = overlay_count #atualizamos a variável de controle da melhor sobreposição da iteração
                    best_overlay_list_count = [i, j] #armazenamos uma lista com os índices das sequências com maior sobreposição; índices relacionados à lista de índices

        superseq = []
        toremove = []
        for i in best_overlay_list_count: #convertemos os índices da lista de índices para os índices da lista de sequências
            aux = seq_list_indexes[i] #pegamos o índice associado na lista de índices
            
            if isinstance(aux, int): #se for um índice inteiro, adicionamos como elemento da lista de supersequência
                superseq.append(aux)
            else: #se for uma sublista de índices, concatenamos com os índices da lista de supersequência
                superseq += aux
            toremove.append(aux) #adicionamos os índices a serem removidos por valor, da lista de índices
        
        for i in toremove: #removemos os índices com maior sobreposição da lista de índices
            seq_list_indexes.remove(i)
            
        seq_list_indexes.append(superseq) #adicionamos a supersequência com maior sobreposição à lista de índices

    return common_supersequence_list(seq_list_indexes[0]), seq_list_indexes[0]

#simulated annealing: heurística aleatória para geração de solução inicial
def random_heuristic(): #gera uma supersequência com ordenação aleatória das sequências
    indexes_order = []

    while(len(indexes_order) < len(sequences_list)):
        new_seq = random.randint(0, len(sequences_list) - 1)
        if new_seq not in indexes_order:
            indexes_order.append(new_seq)
    
    return common_supersequence_list(indexes_order), indexes_order

#grasp: heurística de construção de solução inicial
def grasp_construction(): #constrói a solução inicial, uma lista ordenada de índices; verifica o par com maior sobreposição, escolhido aleatoriamente se houver mais de um; depois verifica um índice por vez, qual o próximo par com maior sobreposição
    best_overlay_count = -1
    constructed_indexes_order = []
    total_indexes_count = len(sequences_list)

    for i in range(0, len(sequences_list)): #geramos uma lista com os pares com maior sobreposição
        for j in range(0, len(sequences_list)):
            if(i == j):
                continue

            overlay_count = overlay(sequences_list[i], sequences_list[j])

            if(best_overlay_count < overlay_count):
                best_overlay_count = overlay_count
                best_overlay_list = [[i, j]]
            elif(best_overlay_count == overlay_count):
                best_overlay_list.append([i, j])

    choosed_pair = random.randint(0, len(best_overlay_list) - 1) #escolhemos aleatoriamente um dos pares, como inicial
    _, next_index = best_overlay_list[choosed_pair] #pegamos o segundo índice do par escolhido
    constructed_indexes_order += best_overlay_list[choosed_pair] #adicionamos o par na nossa lista de índices construída
    
    while(len(constructed_indexes_order) < total_indexes_count): #para quando todos os índices tiverem sido adicionados
        best_overlay_count = -1
        best_overlay_list = []

        for j in range(0, total_indexes_count): #geramos uma lista com os pares com maior sobreposição, sendo next_index o primeiro elemento
            if next_index == j or j in constructed_indexes_order: #ignora índices que já estão na lista de índices construída
                continue

            overlay_count = overlay(sequences_list[next_index], sequences_list[j])

            if(best_overlay_count < overlay_count):
                best_overlay_count = overlay_count
                best_overlay_list.append(j)
            elif(best_overlay_count == overlay_count):
                best_overlay_list.append(j)

        choosed_pair = random.randint(0, len(best_overlay_list) - 1)
        next_index = best_overlay_list[choosed_pair]
        constructed_indexes_order.append(next_index)
        
    return common_supersequence_list(constructed_indexes_order), constructed_indexes_order

if __name__ == "__main__":
    
    sa1, sa_order1 = greedy_algorithm()
    sa2, sa_order2 = random_heuristic()
    grasp, grasp_order = grasp_construction()

    print("greedy_length: ", len(sa1))
    print(sa1)

    print("sa_length: ", len(sa2))
    print(sa2)

    print("grasp_length: ", len(grasp))
    print(grasp)