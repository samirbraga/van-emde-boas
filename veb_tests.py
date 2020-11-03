from veb import VEB
from random import randint


def _test_an_instance(veb: VEB):
    n = 100
    # cria uma lista com números aleatórios
    insertions = list(set([randint(1, 9000) for _ in range(n)]))
    # insere todos na VEB
    for i in insertions:
        veb.insert(i)
    # testa a função ambas as funções 'member' e 'insert'
    for i in insertions:
        assert veb.member(i)

    # seleciona 20 números únicos dentre os inseridos para teste
    tests_indexes = list(set([randint(0, len(insertions) - 1) for _ in range(20)]))
    tests = [insertions[i] for i in tests_indexes]

    # encontra o sucessor de cada número de testes
    successors = [veb.successor(x) for x in tests]

    # remove todos os sucessores escolhidos
    for j in successors:
        veb.remove(j)
    # verifica se os sucessores ainda existem na VEB
    for j in successors:
        assert not veb.member(j)

s
def main():
    # # Repete o teste para 100 instâncias
    # for _ in range(4):
    veb = VEB()
    _test_an_instance(veb)

if __name__ == "__main__":
    main()
