from veb import VEB
from veb_hashtable import Hashtable


def main():
    table = Hashtable(100, 16, 8)
    v1 = VEB()
    v2 = VEB()
    v3 = VEB()
    table.add(1, v1)
    table.add(42, v2)
    table.add(93, v3)

    assert v1 == table.get(1)
    assert v2 == table.get(42)
    assert v3 == table.get(93)

if __name__ == '__main__':
    main()
