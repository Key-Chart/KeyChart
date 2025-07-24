import random

tasks = list(range(1, 18))  # Tasks de 1 a 17
devs = ["Marcus Batista", "Luan Carvalho", "Emanuel Rodriguês"]

# Embaralha as tasks
random.shuffle(tasks)

# Distribui as tasks em modo round-robin para os devs
assignment = {dev: [] for dev in devs}
for i, task in enumerate(tasks):
    dev = devs[i % len(devs)]
    assignment[dev].append(task)

# Função para formatar saída bonita
def print_assignment(assignment):
    print("\n" + "="*60)
    print("🚀 Distribuição Aleatória de Tasks - KeyChart 🚀".center(60))
    print("="*60 + "\n")
    for dev, tasks in assignment.items():
        print(f"👤 {dev}:")
        # Ordena os números para melhor visualização
        for t in sorted(tasks):
            print(f"   📝 Task {t:02d}")
        print("\n" + "-"*60 + "\n")
    print("✨ Boa sorte a todos! ✨".center(60))
    print("="*60 + "\n")

print_assignment(assignment)
