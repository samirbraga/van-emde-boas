from veb import VEB
from random import randint


def main():
    veb = VEB(16)
    insertions = [randint(1, 900) for i in range(1000)]
    for i in insertions:
        veb.insert(i)

    print(insertions)
    print(veb.successor(10))
    print(veb.successor(816))
    print(veb.successor(444))


if __name__ == "__main__":
    main()
