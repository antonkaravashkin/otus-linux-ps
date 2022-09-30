import subprocess
from collections import Counter
from datetime import datetime
import sys

filename = datetime.now().strftime("%d-%m-%Y-%H:%M")+"-scan.txt"
ps = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE,
                      encoding="utf-8").communicate()[0]

output = ps.split('\n')
nfields = len(output[0].split()) - 1

ps_list = []
for row in output[1:]:
    ps_list.append(row.split(None, nfields))


users = list(set([ps[0] for ps in ps_list if ps]))

process_count = 0
for ps in ps_list:
    if ps:
        process_count += 1

user_count = list([ps[0] for ps in ps_list if ps])

user_processess = dict(Counter(user_count))

ram_list = list([float(ps[3]) for ps in ps_list if ps])
cpu_list = list([float(ps[2]) for ps in ps_list if ps])
command_list = list([ps[10][:20] for ps in ps_list if ps])
ram_command_list = list(zip(ram_list, command_list))
cpu_command_list = list(zip(cpu_list, command_list))

file = open(filename, 'a')
sys.stdout = file
print(f"Отчет о состоянии системы:")
print(f"Пользователи системы: {', '.join(str(x) for x in users)}")
print(f"Процессов запущено: {process_count}")
print(f"Пользовательских процессов запущено: ")
for key, value in user_processess.items():
    print(f"{key}: {value}")
print(f"Всего памяти используется: {round(sum(ram_list), 2)}%")
print(f"Всего CPU используется: {round(sum(cpu_list), 2)}%")
print(f"Больше всего памяти использует: %{max(ram_command_list)}")
print(f"Больше всего CPU использует: %{max(cpu_command_list)}")
file.close()
