#import sys
import random
import math
import data_generator as dg
import time

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
    count = 0

    while len(seq_list_indexes) > 1: #o algoritmo para, quando houver apenas uma sublista de índices
        best_overlay_count = -1
        best_overlay_list_count = []
        seq_list_values = [] #lista com as sequências associadas aos elementos da lista de índices

        time_1 = time.time()
        for i in seq_list_indexes: #verificamos a lista de índices de seq; ao final, teremos uma lista com as sequências e não seus indíces
            if(isinstance(i, list)): #se o índice for uma sublista de índices, precisamos da supersequência associada a sublista
                seq_list_values.append(common_supersequence_list(i))
            else: #se for apenas um índice, adicionamos a sequência associada ao índice apenas
                seq_list_values.append(sequences_list[i])
            #print("time_1: ", time.time() - time_1)

        time_2 = time.time()
        for i in range(0, len(seq_list_values)): #buscamos as sequências com maior sobreposição
            for j in range(0, len(seq_list_values)):
                if(i == j):
                    continue

                overlay_count = overlay(seq_list_values[i], seq_list_values[j])
                count += 1

                if(best_overlay_count < overlay_count): #quando duas sequências tiveram a maior sobreposição da iteração
                    best_overlay_count = overlay_count #atualizamos a variável de controle da melhor sobreposição da iteração
                    best_overlay_list_count = [i, j] #armazenamos uma lista com os índices das sequências com maior sobreposição; índices relacionados à lista de índices
            #print("time_2: ", time.time() - time_2)

        superseq = []
        toremove = []
        time_3 = time.time()
        for i in best_overlay_list_count: #convertemos os índices da lista de índices para os índices da lista de sequências
            aux = seq_list_indexes[i] #pegamos o índice associado na lista de índices
            
            if isinstance(aux, int): #se for um índice inteiro, adicionamos como elemento da lista de supersequência
                superseq.append(aux)
            else: #se for uma sublista de índices, concatenamos com os índices da lista de supersequência
                superseq += aux
            toremove.append(aux) #adicionamos os índices a serem removidos por valor, da lista de índices
            #print("time_3: ", time.time() - time_3)
        
        time_4 = time.time()
        for i in toremove: #removemos os índices com maior sobreposição da lista de índices
            seq_list_indexes.remove(i)
            #print("time_4: ", time.time() - time_4)
            
        seq_list_indexes.append(superseq) #adicionamos a supersequência com maior sobreposição à lista de índices
        #print("count: ", count)

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
    changes_count = int(0.5 * len(sequences_list))
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

def find_neighboor_changingWorstOverlays(indexes_order, worst_overlay):
    overlay_list = []
    options_list = []

    for i in range(1, len(indexes_order) - 1):
        overlay_left = overlay(sequences_list[indexes_order[i - 1]], sequences_list[indexes_order[i]])
        overlay_right = overlay(sequences_list[indexes_order[i]], sequences_list[indexes_order[i + 1]])
        sum_overlay = overlay_left + overlay_right
        overlay_list.append(sum_overlay)

    for i in range(0, len(indexes_order) - 2):
        if overlay_list[i] <= worst_overlay:
            options_list.append(i + 1)

    while len(options_list) <= 1:
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

def update_worst_overlay(worst_overlay, is_increasing):
    if worst_overlay == 4 and is_increasing == 1:
        is_increasing = 0
    elif worst_overlay == 0 and is_increasing == 0:
        is_increasing = 1

    if is_increasing == 1:
        worst_overlay += 1
    elif is_increasing == 0:
        worst_overlay -= 1

    return worst_overlay, is_increasing

def simulated_annealing_worstOverlayNeighboor(initial_sequence, initial_indexes_order): #verifica vizinhos com perturbação nos índices que compõe a supersequência atual, caminhando pelo espaço de busca
    t = t_max
    best_sequence, best_indexes_order = initial_sequence, initial_indexes_order
    global_best_length = len(best_sequence)
    global_best_sequence = best_sequence
    global_best_indexes_order = best_indexes_order
    start_time = time.time()
    worst_overlay = 0
    noimprove_weight = 1
    noimprove_time = time.time()
    is_increasing = 1
    time_toChangeOverlay = max_time/12

    max_noimprove_time = 20

    if max_time < max_noimprove_time * 4:
        max_noimprove_time = max_time / 3

    while(t > t_min):
        if noimprove_weight == 3:
            neighboor_sequence, neighboor_indexes_order = find_random_distant_neighboor(best_indexes_order)
            noimprove_weight = 1

        if (time.time() - noimprove_time) >= time_toChangeOverlay:
            noimprove_time = time.time()
            worst_overlay, is_increasing = update_worst_overlay(worst_overlay, is_increasing)

        if (time.time() - noimprove_time) == max_noimprove_time * noimprove_weight:
            neighboor_sequence, neighboor_indexes_order = find_neighboor_changingWorstOverlays(best_indexes_order, worst_overlay)
            noimprove_weight += 1
        else:
            neighboor_sequence, neighboor_indexes_order = find_neighboor_changingWorstOverlays(best_indexes_order, worst_overlay)

        fitness = len(neighboor_sequence) - len(best_sequence)
        probability_coeficient = random.uniform(0.7, 1.0)
        decision_coeficient = math.exp(-fitness/t)
        coeficient_comparison = (probability_coeficient <= decision_coeficient)

        if fitness <= 0 or (fitness > 0 and coeficient_comparison):
            best_sequence, best_indexes_order = neighboor_sequence, neighboor_indexes_order
            if(global_best_length > len(best_sequence)):
                global_best_length = len(best_sequence)
                global_best_sequence = best_sequence
                global_best_indexes_order = best_indexes_order
                noimprove_time = time.time()
                noimprove_weight = 1
                if t <= 2:
                    t = t * 2

        t = t * cooling_coefficient
        running_time = time.time() - start_time

        if running_time > max_time:
            break
    
    return global_best_sequence, global_best_indexes_order

def simulated_annealing_randomNeighboor(initial_sequence, initial_indexes_order): #verifica vizinhos com perturbação nos índices que compõe a supersequência atual, caminhando pelo espaço de busca
    t = t_max
    best_sequence, best_indexes_order = initial_sequence, initial_indexes_order
    global_best_length = len(best_sequence)
    global_best_sequence = best_sequence
    global_best_indexes_order = best_indexes_order
    start_time = time.time()
    noimprove_weight = 1
    noimprove_time = time.time()

    max_noimprove_time = 20

    if max_time < max_noimprove_time * 4:
        max_noimprove_time = max_time / 3

    while(t > t_min):
        if noimprove_weight == 3:
            neighboor_sequence, neighboor_indexes_order = find_random_distant_neighboor(best_indexes_order)
            noimprove_weight = 1

        if (time.time() - noimprove_time) == max_noimprove_time * noimprove_weight:
            neighboor_sequence, neighboor_indexes_order = find_random_neighboor(best_indexes_order)
            noimprove_weight += 1
        else:
            neighboor_sequence, neighboor_indexes_order = find_random_neighboor(best_indexes_order)

        fitness = len(neighboor_sequence) - len(best_sequence)
        probability_coeficient = random.uniform(0.7, 1.0)
        decision_coeficient = math.exp(-fitness/t)
        coeficient_comparison = (probability_coeficient <= decision_coeficient)

        if fitness <= 0 or (fitness > 0 and coeficient_comparison):
            best_sequence, best_indexes_order = neighboor_sequence, neighboor_indexes_order
            if(global_best_length > len(best_sequence)):
                global_best_length = len(best_sequence)
                global_best_sequence = best_sequence
                global_best_indexes_order = best_indexes_order
                noimprove_time = time.time()
                noimprove_weight = 1
                if t <= 2:
                    t = t * 2

        t = t * cooling_coefficient
        running_time = time.time() - start_time

        if running_time > max_time:
            break
    
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

def grasp_worstOverlay():
    worst_overlay = 0
    is_increasing = 1
    _, grasp_initial_order = grasp_construction()
    best_sequence, best_order = find_neighboor_changingWorstOverlays(grasp_initial_order, worst_overlay)
    best_length = len(best_sequence)
    start_time = time.time()
    iter_count = 0

    for i in range(0, max_iter):
        _, grasp_initial_order = grasp_construction()
        new_sequence, new_order = find_neighboor_changingWorstOverlays(grasp_initial_order, worst_overlay)
        new_length = len(new_sequence)
        
        if(best_length > new_length):
            best_length = new_length
            best_sequence = new_sequence
            best_order = new_order

        if iter_count == 5:
            worst_overlay, is_increasing = update_worst_overlay(worst_overlay, is_increasing)
            iter_count = 0
        
        iter_count += 1
        running_time = time.time() - start_time

        if running_time > max_time:
            break

    return best_sequence, best_order

def grasp_betterSubsequentNeighboor():
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
            break

    return best_sequence, best_order

def print_overlay_indexes_order(indexes_order):
    for i in range(0, len(indexes_order)):
        if i + 1 == len(indexes_order):
            break
        print(overlay(sequences_list[indexes_order[i]], sequences_list[indexes_order[i + 1]]), end=" ")
    print()

def concatenation_supersequence():
    length_count = 0
    for i in range(0, len(sequences_list)):
        length_count += len(sequences_list[i])
    return length_count

if __name__ == "__main__":

    sequences_list = dg.get_data("samples/samples-100_100.txt")

    t_min = 1
    t_max = 10
    cooling_coefficient = 0.99999
    max_iter = 1200
    max_time = 30 # multiplicado por três, pois são três metaheurísticas rodando (aproximadamente)
    print("SOLUTION\t\t\tLENGTH\tDISTANCE TO SUM OF ALL SEQUENCES")

    total_length = concatenation_supersequence()
    print("sum_sequences_length \t\t", total_length, "\t\t\t", 0)

    solution1, order1 = greedy_algorithm()
    print("greedy_length \t\t\t", len(solution1), "\t\t\t", total_length - len(solution1))
    random_start_sequence, random_start_indexes_order = random_heuristic()
    solution2, order2 = simulated_annealing_worstOverlayNeighboor(random_start_sequence, random_start_indexes_order)
    print("sa1_length \t\t\t", len(solution2), "\t\t\t", total_length - len(solution2))
    #print("random_heuristic_length \t", len(random_start_sequence), "\t\t\t", total_length - len(random_start_sequence))
    solution3, order3 = simulated_annealing_randomNeighboor(random_start_sequence, random_start_indexes_order)
    print("sa2_length \t\t\t", len(solution3), "\t\t\t", total_length - len(solution3))
    solution4, order4 = grasp_betterSubsequentNeighboor()
    print("grasp1_length \t\t\t", len(solution4), "\t\t\t", total_length - len(solution4))
    solution5, order5 = grasp_worstOverlay()
    print("grasp2_length \t\t\t", len(solution5), "\t\t\t", total_length - len(solution5))


'''
if __name__ == "__main__":

    sample_list = ["samples/samples-100_100.txt"]
    #"samples/samples-50_20.txt", "samples/samples-50_50.txt", "samples/samples-50_100.txt", 
    #max_time_list = [10, 30, 60]
    max_time_list = [90, 120]
    #max_time_list = [1, 1]
    execution_times = 1
    t_min = 1
    t_max = 10
    cooling_coefficient = 0.99999
    max_iter = 1200
    results_file = "results2.csv"
    #sequences_list = ["aaa", "aab", "abb", "bba", "baa", "bbb"]
    #sequences_list = dg.get_data("samples.txt")
    
    #sigma = 0.09
    #t_max = 100
    #t_min = 0.0005
    

    data_file = open(results_file, "w")
    data_file.writelines("MÉTODO; COMPRIMENTO DA SUPERSEQUÊNCIA COMUM; DISTÂNCIA PARA A SUPERSEQUÊNCIA COMUM MAIS SIMPLES; TEMPO DE EXECUÇÃO;\n")
    for i in sample_list:
        sequences_list = dg.get_data(i)
        random_start_sequence, random_start_indexes_order = random_heuristic()
        time1 = time.time()
        total_length = concatenation_supersequence()
        time2 = time.time()
        greedy, _ = greedy_algorithm()
        time3 = time.time()

        data_file.writelines("simplier; " + str(total_length) + "; " + str(total_length - total_length) + "; " + str(round(time2 - time1, 3)) + "s;\n")
        data_file.writelines("greedy; " + str(len(greedy)) + "; " + str(total_length - len(greedy)) + "; " + str(round(time3 - time2, 3)) + "s;\n")

        for j in max_time_list:
            max_time = j
            data_file.writelines("TEMPO; " + str(max_time) + ";;\n")

            for k in range(0, execution_times):
                data_file.writelines("RODADA; " + str(k + 1) + ";;\n")
                time1 = time.time()
                sa1, _ = simulated_annealing_worstOverlayNeighboor(random_start_sequence, random_start_indexes_order)
                time2 = time.time()
                #sa2, _ = simulated_annealing_randomNeighboor(random_start_sequence, random_start_indexes_order)
                time3 = time.time()
                grasp1, _ = grasp_betterSubsequentNeighboor()
                time4 = time.time()
                #grasp2, _ = grasp_worstOverlay()
                time5 = time.time()
                data_file.writelines("sa 1; " + str(len(sa1)) + "; " + str(total_length - len(sa1)) + "; " + str(round(time2 - time1, 3)) + "s;\n")
                #data_file.writelines("sa 2; " + str(len(sa2)) + "; " + str(total_length - len(sa2)) + "; " + str(round(time3 - time2, 3)) + "s;\n")
                data_file.writelines("grasp 1; " + str(len(grasp1)) + "; " + str(total_length - len(grasp1)) + "; " + str(round(time4 - time3, 3)) + "s;\n")
                #data_file.writelines("grasp 2; " + str(len(grasp2)) + "; " + str(total_length - len(grasp2)) + "; " + str(round(time5 - time4, 3)) + "s;\n")

    data_file.close()
'''