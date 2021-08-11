#import sys
import random
import math
import data_generator as dg
import time

#sequences_list = ["aaa", "aab", "abb", "bba", "baa", "bbb"]
sequences_list = dg.get_data("samples.txt")

'''
sigma = 0.09
t_max = 100
t_min = 0.0005
'''

t_min = 1
t_max = 15
cooling_coefficient = 0.99999
max_iter = 1000
max_time = 20 # multiplicado por três, pois são três metaheurísticas rodando (aproximadamente)

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

def random_heuristic(): #gera uma supersequência com ordenação aleatória das sequências
    indexes_order = []

    while(len(indexes_order) < len(sequences_list)):
        new_seq = random.randint(0, len(sequences_list) - 1)
        if new_seq not in indexes_order:
            indexes_order.append(new_seq)
    
    return common_supersequence_list(indexes_order), indexes_order

def find_random_neighboor(indexes_order): #encontra uma sequência vizinha, alterando a posição dos índices usados para formar a supersequência
    rand_sequence = random.randint(0, len(indexes_order) - 2) #vizinho será obtido alterando a posição de uma sequência com outra sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
    new_order = [] + indexes_order
    new_order[rand_sequence] = indexes_order[rand_sequence + 1]
    new_order[rand_sequence + 1] = indexes_order[rand_sequence]

    return common_supersequence_list(new_order), new_order

def find_random_distant_neighboor(indexes_order): #encontra uma sequência vizinha, alterando 10% das posição dos índices usados para formar a supersequência
    changes_count = int(0.1 * len(sequences_list))
    already_changed = []

    while changes_count > -1:
        rand_sequence = random.randint(0, len(indexes_order) - 2) #vizinho será obtido alterando a posição de uma sequência com outra sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
        if rand_sequence not in already_changed:
            already_changed.append(rand_sequence)
            new_order = [] + indexes_order
            new_order[rand_sequence] = indexes_order[rand_sequence + 1]
            new_order[rand_sequence + 1] = indexes_order[rand_sequence]
            changes_count -= 1

    return common_supersequence_list(new_order), new_order

def find_interesting_neighboor(indexes_order, worst_overlay):
    overlay_list = []
    options_list = []

    for i in range(1, len(indexes_order) - 1):
        overlay_left = overlay(sequences_list[indexes_order[i - 1]], sequences_list[indexes_order[i]])
        overlay_right = overlay(sequences_list[indexes_order[i]], sequences_list[indexes_order[i + 1]])
        total_overlay = overlay_left + overlay_right
        overlay_list.append(total_overlay)
    
    #for i in range(0, len(indexes_order) - 2):
        #print(i + 1, ": ", overlay_list[i], overlay_list[i][0] + overlay_list[i][1])

    for i in range(0, len(indexes_order) - 2):
        if overlay_list[i] <= worst_overlay:
            options_list.append(i + 1)

    while options_list == []:
        worst_overlay += 1
        for i in range(0, len(indexes_order) - 2):
            if overlay_list[i] <= worst_overlay:
                options_list.append(i + 1)
    
    rand_sequence_1 = random.randint(0, len(options_list) - 1) #vizinho será obtido alterando a posição de uma sequência com outra sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
    rand_sequence_2 = rand_sequence_1

    while rand_sequence_2 == rand_sequence_1:
        rand_sequence_2 = random.randint(0, len(options_list) - 1)

    #print("worst: ", worst_overlay)
    #print("overlay1: ", overlay_list[options_list[rand_sequence_1] - 1], options_list[rand_sequence_1])
    #print("overlay2: ", overlay_list[options_list[rand_sequence_2] - 1], options_list[rand_sequence_2])
    new_order = [] + indexes_order
    new_order[options_list[rand_sequence_1]] = indexes_order[options_list[rand_sequence_2]]
    new_order[options_list[rand_sequence_2]] = indexes_order[options_list[rand_sequence_1]]

    return common_supersequence_list(new_order), new_order

def simulated_annealing(initial_sequence, initial_indexes_order): #verifica vizinhos com perturbação nos índices que compõe a supersequência atual, caminhando pelo espaço de busca
    t = t_max
    #best_sequence, best_indexes_order = greedy_algorithm() #solução gerada pelo algoritmo guloso que resolve o problema
    #random_heuristic() #solução inicial gerada por uma heurística aleatória
    best_sequence, best_indexes_order = initial_sequence, initial_indexes_order
    global_best_length = len(best_sequence)
    global_best_sequence = best_sequence
    global_best_indexes_order = best_indexes_order
    noimprove_count = 0
    start_time = time.time()

    #print("length: ", global_best_length)
    #print_overlay_indexes_order(initial_indexes_order)

    prob_count = 0
    dec_count = 0
    worst_overlay = 1
    noimprove_weight = 1

    while(t > t_min):
        if noimprove_weight == 2:
            #print("neighboor reset")
            #print("noimprove_iter:", noimprove_count)
            #print("worst_overlay: ", worst_overlay)
            #print("time: ", t)
            neighboor_sequence, neighboor_indexes_order = initial_sequence, initial_indexes_order
            #worst_overlay = 1 #talvez não resetar
            noimprove_weight = 1
            noimprove_count = 0
            t = t * 1.5

        if noimprove_count == (noimprove_weight * max_time * 300):
            t = t * 1.2
            worst_overlay += 1
            #print("worst overlay increment")
            #print("noimprove_iter:", noimprove_count)
            #print("worst_overlay: ", worst_overlay)
            #print("time: ", t)
            #print("length: ", len(neighboor_sequence))
            #print_overlay_indexes_order(neighboor_indexes_order)
            #neighboor_sequence, neighboor_indexes_order = find_random_distant_neighboor(best_indexes_order)
            neighboor_sequence, neighboor_indexes_order = find_interesting_neighboor(best_indexes_order, worst_overlay)
            noimprove_weight += 1
            #noimprove_count = 0
        else:
            neighboor_sequence, neighboor_indexes_order = find_interesting_neighboor(best_indexes_order, worst_overlay)
            #neighboor_sequence, neighboor_indexes_order = find_random_neighboor(best_indexes_order)

        #pause = input()
        fitness = len(neighboor_sequence) - len(best_sequence)
        probability_coeficient = random.uniform(0.7, 1.0)
        decision_coeficient = math.exp(-fitness/t)
        coeficient_comparison = (probability_coeficient <= decision_coeficient)

        if coeficient_comparison == True:
            dec_count += 1
        else:
            prob_count += 1

        #if fitness > 0:
            #print("prob: ", probability_coeficient)
            #print("dec:  ", decision_coeficient)
            #print("fit:  ", fitness)
            #print("time: ", t)
            #print(coeficient_comparison)
            #pause = input()

        if fitness <= 0 or (fitness > 0 and coeficient_comparison):
            best_sequence, best_indexes_order = neighboor_sequence, neighboor_indexes_order
            if(global_best_length > len(best_sequence)):
                global_best_length = len(best_sequence)
                global_best_sequence = best_sequence
                global_best_indexes_order = best_indexes_order
                #print("improve_iter:", noimprove_count)
                noimprove_count = 0
                noimprove_weight = 1
                #print("dec: ", dec_count, "prob: ", prob_count, "time: ", t, "length: ", global_best_length)
                dec_count = 0
                prob_count = 0
                #print("global change")
                #print("running_time:", time.time() - start_time)
                #print("length: ", global_best_length)
                #print("time: ", t)
                #print_overlay_indexes_order(best_indexes_order)
            else:
                noimprove_count += 1
        else:
            noimprove_count += 1
        t = t * cooling_coefficient
        #t = t * random.uniform(0.8, 0.99)
        #t = t * (math.exp((random.uniform(0.1, 0.9) * -t)/sigma)) 

        running_time = time.time() - start_time

        if running_time > max_time:
            break
    #print("running_time:", running_time)
    #print("noimprove_count:", noimprove_count)
    #print("-------------------")
    return global_best_sequence, global_best_indexes_order

def find_grasp_neighboor_sequence(indexes_order): #encontra a melhor sequência vizinha, modificando os índices dois a dois
    best_indexes_order = [] + indexes_order #lista ordenada de índices da solução inicial
    best_length = len(common_supersequence_list(best_indexes_order)) #comprimento da supersequência associada a lista ordenada de índices da solução inicial

    for i in range(0, len(indexes_order) - 1):
        modified_indexes_order = [] + best_indexes_order
        modified_indexes_order[i] = best_indexes_order[i + 1] #trocamos o índice i de modified_indexes_order pelo índice i+1
        modified_indexes_order[i + 1] = best_indexes_order[i]

        new_sequence = common_supersequence_list(modified_indexes_order)
        new_length = len(new_sequence)

        if new_length < best_length:
            best_indexes_order = modified_indexes_order
            best_length = new_length

    return common_supersequence_list(best_indexes_order), best_indexes_order

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

def grasp_localsearch(grasp_initial, grasp_initial_order): #verifica se os vizinhos são melhores que a solução inicial
    best_length = len(grasp_initial)
    best_sequence = grasp_initial
    best_indexes_order = grasp_initial_order

    best_neighboor_sequence, best_neighboor_order = find_grasp_neighboor_sequence(grasp_initial_order) #verifica entre os vizinhos qual o melhor
    best_neighboor_length = len(best_neighboor_sequence)

    if best_length > best_neighboor_length: #se o melhor vizinho tiver comprimento menor que a solução inicial, atualiza
        best_length = best_neighboor_length
        best_sequence = best_neighboor_sequence
        best_indexes_order = best_neighboor_order

    return best_sequence, best_indexes_order

def grasp():
    grasp_initial, grasp_initial_order = grasp_construction()
    best_sequence, best_order = grasp_localsearch(grasp_initial, grasp_initial_order)
    best_length = len(best_sequence)
    start_time = time.time()

    for i in range(0, max_iter):
        grasp_initial, grasp_initial_order = grasp_construction()
        new_sequence, new_order = grasp_localsearch(grasp_initial, grasp_initial_order)
        new_length = len(new_sequence)
        
        if(best_length > new_length):
            best_length = new_length
            best_sequence = new_sequence
            best_order = new_order
        
        running_time = time.time() - start_time

        if running_time > max_time:
            #print("running_time:", running_time)
            break

    return best_sequence, best_order

def print_overlay_indexes_order(indexes_order):
    for i in range(0, len(indexes_order)):
        if i + 1 == len(indexes_order):
            break
        print(overlay(sequences_list[indexes_order[i]], sequences_list[indexes_order[i + 1]]), end=" ")
    print()

if __name__ == "__main__":

    print("SOLUTION\t\t\tLENGTH\tDISTANCE TO SUM OF ALL SEQUENCES")

    length_count = 0
    for i in range(0, len(sequences_list)):
        length_count += len(sequences_list[i])
    print("sum_sequences_length \t\t", length_count, "\t\t\t", 0)

    solution1, order1 = greedy_algorithm()
    print("greedy_length \t\t\t", len(solution1), "\t\t\t", length_count - len(solution1))
    #solution2, order2 = simulated_annealing(solution1, order1) #sa1: start: greedy
    #print("sa1_length_greedy \t\t", len(solution2), "\t\t\t", length_count - len(solution2))
    random_start_sequence, random_start_indexes_order = random_heuristic()
    print("random_heuristic_length \t", len(random_start_sequence), "\t\t\t", length_count - len(random_start_sequence))
    solution3, order3 = simulated_annealing(random_start_sequence, random_start_indexes_order) #sa1: start: random
    print("sa2_length_random \t\t", len(solution3), "\t\t\t", length_count - len(solution3))
    solution4, order4 = grasp()
    print("grasp_length \t\t\t", len(solution4), "\t\t\t", length_count - len(solution4))

    #print(solution1)
    
    #print_overlay_indexes_order(order1)
    #print_overlay_indexes_order(random_start_indexes_order)
    

    #interesting_sequence, interesting_order = find_interesting_neighboor(random_start_indexes_order)
    #print("interesting_neighboor_length \t", len(interesting_sequence), "\t\t\t", length_count - len(interesting_sequence))
    #print_overlay_indexes_order(interesting_order)

    #print(solution2)

    #print(solution3)

    #print(solution4)

'''
seções:
introdução
revisão da literatura --- subseção: aplicações no mundo real
metodologias usadas (gerador incluso)
resultados
conclusão

relatório - tabela (marcar as melhores soluções/comparar pelo tempo gasto) - média das soluções - no mínimo 3 execuções - tempo
sa_1
sa_2
grasp
greedy
'''