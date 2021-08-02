#import sys
import random
import math

def get_data(data_file):
    data_file = open(data_file, "r")
    sequences_set = data_file.readlines()
    length_count = 0
    for i in range(0, len(sequences_set)):
        sequences_set[i] = sequences_set[i].replace("\n", "")
        length_count += len(sequences_set[i])
    print("total_length:", length_count)
    data_file.close()
    return sequences_set

def common_supersequence(sequence_1, sequence_2):
    overlay_count = overlay(sequence_1, sequence_2) #calculamos a quantidade de sobreposição possível na sequência
    return sequence_1 + sequence_2[overlay_count:len(sequence_2)] #retornamos a string que concatena as sequências, desconsiderando os char iniciais da seq2, envolvidos na sobreposição

def commom_supersequence_list(sequences_set, order):
    overlay_seq = sequences_set[order[0]]
    for j in range(1, len(order)):
        overlay_seq = common_supersequence(overlay_seq, sequences_set[order[j]]) #calculamos a superseq das seqs
    #print(overlay_seq)
    return overlay_seq

def overlay(sequence_1, sequence_2):
    last_char_1 = len(sequence_1) - 1
    if len(sequence_2) >= len(sequence_1):
        last_char_2 = len(sequence_1) - 1 #se a seq2 for maior, "cortamos" os caracteres excedentes; se igual, tanto faz qual comprimento usar
    elif len(sequence_2) < len(sequence_1):
        last_char_2 = len(sequence_2) - 1 #se a seq2 for menor, utilizamos o próprio comprimento

    count = 0
    while count == 0 and last_char_2 > -1:
        aux1 = last_char_1 #para não perder o comprimento da seq1 e evitar o calculo de len()

        for i in range(last_char_2, -1, -1):
            if sequence_1[aux1] == sequence_2[i]: #char igual, incrementa o contador de sobreposição e decrementa o contador de char de seq1
                count += 1
                aux1 -= 1
            else: #a sobreposição não funcionou, contador é zerado para a próxima iteração
                count = 0
                break
        
        last_char_2 -= 1
        
    return count

def overlay_first_heuristic(sequences_set):
    heuristic_set_index = list(range(0, len(sequences_set)))

    while len(heuristic_set_index) > 1:
        max_overlay = -1
        max_overlay_set = []
        heuristic_set_value = []

        for i in heuristic_set_index: #verificamos a lista de índices de seq
            if(isinstance(i, list)): #se o índice for uma lista de índices de seq
                heuristic_set_value.append(commom_supersequence_list(sequences_set, i))
            else:
                heuristic_set_value.append(sequences_set[i])
        #ao final, teremos uma lista com as sequências e não seus indíces
        
        #print(heuristic_set_index)
        #print(heuristic_set_value)

        for i in range(0, len(heuristic_set_value)): #buscamos as sequências com maior sobreposição
            for j in range(0, len(heuristic_set_value)):
                if(i == j):
                    continue

                overlay_count = overlay(heuristic_set_value[i], heuristic_set_value[j])

                if(max_overlay < overlay_count):
                    max_overlay = overlay_count
                    max_overlay_set = [[i, j]]
                #elif(max_overlay == overlay_count):
                #    max_overlay_set.append([i, j])
            #endfor
        #endfor

        '''if(len(max_overlay_set) > 1):
            sequence_choosed = random.randint(0, len(max_overlay_set) - 1)
        else:
            sequence_choosed = 0'''

        superseq = []
        toremove = []
        #print("MAX", max_overlay_set[0])
        for i in max_overlay_set[0]:
            aux = heuristic_set_index[i]
            if isinstance(aux, int):
                superseq += [aux]
            else:
                superseq += aux
            #print("SS", superseq)
            toremove.append(aux)
        #print("REMOVE", toremove)
        for i in toremove:
            #print(i)
            #aux = heuristic_set_index[i]
            #print(aux)
            heuristic_set_index.remove(i)
            
        heuristic_set_index.append(superseq)
    #endwhile    

    #print("FINAL", heuristic_set_index)
    overlay_seq = commom_supersequence_list(sequences_set, heuristic_set_index[0])
    #print(overlay_seq)

    return overlay_seq, heuristic_set_index[0]

def random_heuristic(sequences_set):
    order = []
    
    while(len(order) < len(sequences_set)):
        new_seq = random.randint(0, len(sequences_set) - 1)
        if new_seq not in order:
            order.append(new_seq)

    #print(order)
    
    return commom_supersequence_list(sequences_set, order), order

'''def grasp_construction():
    heuristic_set_index = list(range(0, len(sequences_set)))
    random.randint(0, len(sequences_set))



    while len(heuristic_set_index) > 1:
        max_overlay = -1
        max_overlay_set = []
        heuristic_set_value = []

        for i in heuristic_set_index: #verificamos a lista de índices de seq
            if(isinstance(i, list)): #se o índice for uma lista de índices de seq
                heuristic_set_value.append(commom_supersequence_list(sequences_set, i))
            else:
                heuristic_set_value.append(sequences_set[i])
        #ao final, teremos uma lista com as sequências e não seus indíces
        
        #print(heuristic_set_index)
        #print(heuristic_set_value)

        for i in range(0, len(heuristic_set_value)): #buscamos as sequências com maior sobreposição
            for j in range(0, len(heuristic_set_value)):
                if(i == j):
                    continue

                overlay_count = overlay(heuristic_set_value[i], heuristic_set_value[j])

                if(max_overlay < overlay_count):
                    max_overlay = overlay_count
                    max_overlay_set = [[i, j]]
                #elif(max_overlay == overlay_count):
                #    max_overlay_set.append([i, j])
            #endfor
        #endfor
'''

#def grasp_localsearch()

def find_random_neighboor_sequence(sequences_set, sequence_order):
    rand_sequence = random.randint(0, len(sequence_order) - 2) #vizinho será obtido alterando a posição de uma sequência à direita; assim a última sequência da lista não trocará com ngm (a não ser q a seq anterior a ela faça isso)
    new_order = [] + sequence_order
    new_order[rand_sequence] = sequence_order[rand_sequence + 1]
    new_order[rand_sequence + 1] = sequence_order[rand_sequence]

    return commom_supersequence_list(sequences_set, new_order), new_order

def simulated_annealing(sequences_set, t_min, t_max):
    t = t_max
    #best_sequence, best_order = overlay_first_heuristic(sequences_set)
    best_sequence, best_order = random_heuristic(sequences_set)
    print("greedy_length: ", len(best_sequence))
    print(best_sequence)
    
    better = 1200
    count_equal = 0
    while(t > t_min):
        neighboor_sequence, neighboor_order = find_random_neighboor_sequence(sequences_set, best_order)
        fitness = len(neighboor_sequence) - len(best_sequence)

        probability_coeficient = random.uniform(0.0, 1.0)
        decision_coeficient = math.exp(-fitness/t)

        count_equal += 1
        if fitness <= 0 or (fitness > 0 and probability_coeficient <= decision_coeficient):
            best_sequence, best_order = neighboor_sequence, neighboor_order
            count_equal = 0
            if(better > len(best_sequence)):
                better = len(best_sequence)


        t = t * random.uniform(0.8, 0.99)
        #t = t * (math.exp((random.uniform(0.1, 0.9) * -t)/sigma)) 
    #print(count_equal)
    print("better_length: ", better)
    #print(better)
    print("sa_length: ", len(best_sequence))
    print(best_sequence)
    return best_sequence, best_order

if __name__ == "__main__":
    '''
    sigma = 0.09
    t_max = 100
    t_min = 0.0005
    '''
    t_min = 0.1
    t_max = 1000000000

    sequences_set = ["aaa", "aab", "abb", "bba", "baa", "bbb"]
    random_heuristic(sequences_set)
    #overlay_first_heuristic(["abbb", "bab", "bba"])
    #print(sequences_set)
    
    #sequences_set = get_data("scs_problem_samples.txt")
    #msc, order = simulated_annealing(sequences_set, t_min, t_max)
    #print(common_supersequence("bba", "bab"))
    #print([1,2] + [3,4])

    #print(msc, order, "length: ", len(msc))


'''a = "aaa"
b = "aab"

print(a.find(b[:1], 0))

#greedy algorithm'''
'''
ALGORITHM MAJORITY-MERGE
1. Input: n sequences, each of length n.
2. Set supersequence s := null string;
3. Let a be the majority among the leftmost letters of the remaining sequences. Set
s :-- sa and delete the front a from these sequences. Repeat this step until no
sequences are left.
4. Output s.
'''
'''
samples_file = open("sample.txt", "r")

sequence_set = samples_file.readlines()
sequence_set = [i.replace("\n", "") for i in sequence_set]

bigger_sequence = ""
bigger_length = -1

scs = ""

for sequence in sequence_set:
    if(len(sequence) > bigger_length):
        bigger_sequence = sequence
        bigger_length = len(sequence)

sequence_set.remove(bigger_sequence)
scs = bigger_sequence

###

print(bigger_length, bigger_sequence)

print(sequence_set)

samples_file.close()
'''
'''
scs = sequence[0]

for i in range(1, len(sequence)):
    new_scs = shortest_common_supersequence(sequence[i], scs)
    scs = new_scs

return scs

'''
'''
def shortest_common_supersequence(sequence_1, sequence_2):
    for i in sequence_1:
        for j in sequence_2:
            if(i == )



abbb, bab = 1
abbb, bba = 2
bab, abbb = 2
bab, bba = 1
bba, abbb = 1
bba, bab = 2


abbab


aaa
aab



S = [S1, S2, ..., Sn]   //S é a lista com as sequências
MSC = &                 //MSC é a menor supersequência comum encontrada, inicia-se como sequência vazia

R = S                   //R é a lista de sequências e supersequências ao qual será analisada a quantidade de sobreposição possível, inicia-se com S

faça
{
    matriz_sobreposição = sobreposição_sequências(R)    // matriz com o valor de sobreposição entre os elementos de R
    
    x, y = maior_sobreposição(matriz_sobreposição)      // escolhe as sequências com maior valor de sobreposição; caso haja mais de uma, a escolha é aleatória

    SC = supersequência_comum(R[x], R[y])               // encontra uma supersequência comum entre as sequências R[x] e R[y]

    atualização_R(R[x], R[y], SC)                       // remove as sequências R[x] e R[y] de R e adiciona a supersequência entre elas, SC

} enquanto |R| > 1                                      // a quantidade de elementos de R for maior que 1

MSC = R[0]              //MSC recebe o único elemento de R, a menor supersequência comum encontrada para o conjunto

sobreposição_sequências(R)
{
    matriz_sobreposição = [length(R)][length(R)]    //matriz_sobreposição é a matriz que conterá os valores de sobreposição entre os elementos de R

    for i in range(0, length(R))
    {
        for j in range(0, length(R))
        {
            if(R[i] == R[j])
                matriz_sobreposição[i][j] = -1 //não consideramos a sobreposição da sequência com ela mesma
            else
            {

            }
        }
    }
    
            
}
'''
# (k - 1) * m * n * n



