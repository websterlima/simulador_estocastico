from rand import rand
from time import time

import csv, math

def get_in_interval(interval, t, value):
    for idx, i in enumerate(interval):
        if i[0] <= value < i[1]:
            return t[idx]

intervalos1 = [[0.0, 0.52], [0.52, 0.80], [0.80, 0.90], [0.90, 0.96], [0.96, 1.0]]
tec = [1, 3, 5, 7, 9]

intervalos2 = [[0.0, 0.5], [0.5, 0.82], [0.82, 0.9], [0.9, 0.99], [0.99, 1.0]]
ts = [1.25, 3.75, 6.25, 8.75, 11.25]



'''
TEC 0
TS 1
TREAL 2
TINICIO 3
TFIM 4
TFILA 5
TSISTEMA 6
N PESSOAS 7
TEMPO LIVRE 8
'''

n = 100
rounds = 120

v_m_tec = []
v_m_ser = []
v_m_wait = []
v_m_sys = []

# with open('table1.csv', 'w') as csv_file:

#     writer = csv.writer(csv_file, delimiter=';')

#     writer.writerow(['TEC', 'TS', 'TREAL', 'TINICIO', 'TFIM', 'TFILA', 'TSISTEMA', 'N PESSOAS', 'T LIVRE'])

for r in range(0, rounds):
    queue = []
    table = []

    for i in range(0, n):
        t_tec = get_in_interval(intervalos1, tec, rand(time()))
        t_ts = get_in_interval(intervalos2, ts, rand(time()))


        if not table:
            line = [t_tec, t_ts, t_tec, t_tec, t_tec + t_ts, 0, t_ts, 0, t_tec]
        else:
            prev = table[i - 1]

            t_real = prev[2] + t_tec
            t_init = max(prev[4], t_real)
            t_end = t_init + t_ts
            t_queue = max(prev[4] - t_real, 0)
            t_sys = t_queue + t_ts

            while queue and queue[0] <= t_real:
                queue = queue[1:]

            if t_real < prev[4]:
                queue.append(t_init)

            n_queue = len(queue)
            # n_queue = max(prev[7] + (1 if t_real < prev[4] else (-1 if t_real > prev[4] else 0)), 0)
            t_free = 0 if prev[4] > t_real else t_real - prev[4]

            line = [t_tec, t_ts, t_real, t_init, t_end, t_queue, t_sys, n_queue, t_free]

        table.append(line)
        # writer.writerow(line)

    p_free = 0.0
    m_tec = 0.0
    m_ser = 0.0
    m_wait = 0.0
    p_wait = 0.0
    m_sys = 0.0

    for line in table:
        p_free += line[8]
        m_tec += line[0]
        m_ser += line[1]
        m_wait += line[5]
        p_wait += 1 if line[5] > 0 else 0
        m_sys += line[6]

    p_free /= table[-1:][0][4]
    m_tec /= n
    m_ser /= n
    m_wait /= n
    p_wait /= n
    m_sys /= n

    v_m_tec.append(m_tec)
    v_m_ser.append(m_ser)
    v_m_wait.append(m_wait)
    v_m_sys.append(m_sys)

def media(vector):
    return sum(vector) / len(vector)

def variancia(vector):
    return (sum(map(lambda x: x ** 2, vector)) - (sum(vector) ** 2) / len(vector)) / (len(vector) - 1)

def intervalo_confianca(media, variancia, n, t_st):
    interval = t_st * (math.sqrt(variancia) / math.sqrt(n))
    return [media - interval, media + interval]

print v_m_tec[:5]

m_tec = media(v_m_tec)
m_ser = media(v_m_ser)
m_wait = media(v_m_wait)
m_sys = media(v_m_sys)

var_m_tec = variancia(v_m_tec)
var_m_ser = variancia(v_m_ser)
var_m_wait = variancia(v_m_wait)
var_m_sys = variancia(v_m_sys)

i_m_tec = intervalo_confianca(m_tec, var_m_tec, len(v_m_tec), 1.96)
i_m_ser = intervalo_confianca(m_ser, var_m_ser, len(v_m_ser), 1.96)
i_m_wait = intervalo_confianca(m_wait, var_m_wait, len(v_m_wait), 1.96)
i_m_sys = intervalo_confianca(m_sys, var_m_sys, len(v_m_sys), 1.96)


print 'tec %f <= u <= %f' % (i_m_tec[0], i_m_tec[1])
print 'ser %f <= u <= %f' % (i_m_ser[0], i_m_ser[1])
print 'wait %f <= u <= %f' % (i_m_wait[0], i_m_wait[1])
print 'sys %f <= u <= %f' % (i_m_sys[0], i_m_sys[1])


# print 'Probabilidade de caixa livre %.2f' % p_free
# print 'Tempo medio entre as chegadas %.2f' % m_tec
# print 'Tempo medio de servico %.2f' % m_ser
# print 'Tempo medio de espera na fila %.2f' % m_wait
# print 'Probabilidade de um cliente esperar na fila %.2f' % p_wait
# print 'Tempo medio despendido no sistema %.2f' % m_sys

'''
0.01
2.59
3.16
32.08
10.6
35.24
'''

