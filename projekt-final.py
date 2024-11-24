import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def dane():
    print("Witaj Podrózniku! Program pomoze ci wybrać schroniska do którcyh moęsz bezpiecznie dotrzeć podczas twojej wyprawy.")
    # Użytkownik wybiera, czy chce podać dane ręcznie, czy wylosować graf
    try:
        wybór = int(input("Wybierz opcję: 1 - Podaj własne dane, 2 - Wygeneruj losowy graf: "))
        if wybór == 1:
            n = int(input("Podaj liczbę schronisk: "))
            print("Podaj macierz nxn, symetryczną, z zerami na głównej przekątnej (odzwierciedlającą istnienie szlaków jako niezerowe liczby oraz ich wysokość jako wartość liczby) jako wiersze liczb oddzielonych spacjami (n x n):")
            graf = []
            for i in range(n):
                wiersz = list(map(int, input(f"Wiersz {i+1}: ").split()))
                if len(wiersz) != n:
                    raise ValueError("Macierz musi mieć rozmiar nxn!")
                graf.append(wiersz)
            for i in range(n):
                if graf[i][i] != 0:
                   raise Exception("Nie może istnieć szlak do tego samego schroniska!") 
                for j in range(n):
                    if graf[i][j] != graf[j][i]:
                        raise Exception("Macierz musi być symetryczna!")

            nazwy = []
            print("Podaj nazwy schronisk (po jednej na wiersz):")
            for i in range(n):
                nazwa = input(f"Nazwa dla wierzchołka {i+1}: ")
                nazwy.append(nazwa)

            Wmax = int(input("Podaj maksymalną wysokość szlaku (Wmax): "))
            if Wmax <= 0:
                raise Exception("Wysokość musi być liczbą dodatnią.")
            
            numer = int(input("Podaj numer wierzchołka startowego: "))
            if numer < 0 or numer >= n:
                raise Exception("Numer wierzchołka startowego musi być >= 0 i < ", n)
            
            return graf, nazwy, Wmax, numer

        elif wybór == 2:
            n = int(input("Podaj liczbę wierzchołków (n): "))
            m = int(input("Podaj liczbę krawędzi (m): "))

            if m < n - 1:
                raise Exception("Graf będzie niespójny. Podaj liczbę >= n-1")
            if m > n * (n - 1) / 2:
                raise Exception("Za dużo krawędzi w grafie.")
            
            Wmax = int(input("Podaj maksymalną wysokość szlaku (Wmax): "))
            if Wmax <= 0:
                raise Exception("Wysokość musi być liczbą dodatnią.")
            
            W = int(input("Podaj największą wysokość jaka ma być w grafie (W): "))
            if W < Wmax:
                raise Exception("Wysokość W musi być większa lub równa Wmax")
            
            numer = int(input("Podaj numer wierzchołka startowego: "))
            if numer < 0 or numer >= n:
                raise Exception("Numer wierzchołka startowego musi być >= 0 i < ", n)
            
            graf, nazwy = los_graf(n, m, W)
            return graf, nazwy, Wmax, numer
            
        else:
            raise Exception("Nieprawidłowy wybór.")
    except Exception as e:
        print("Błąd:", e)
        exit(1)

def los_graf(n, m, W):   
    graf = [[0 for i in range(n)] for j in range(n)]

    # Losowanie nazw schronisk
    nazwy = los_nazwy(n)

    # Lista wierzchołków, które po kolei łączy ścieżka - robimy graf rozpinający
    lista = random.sample(range(n), n)
    for i in range(n-1):
        elem1 = lista[i]
        elem2 = lista[i+1]
        wys = random.randint(1, W)
        graf[elem1][elem2], graf[elem2][elem1] = wys, wys

    dodatkowe_krawedzie = m - (n - 1)
    while dodatkowe_krawedzie > 0:
        k = random.randint(0, n-1)
        l = random.randint(0, n-1)
        if k != l and graf[k][l] == 0:
            wys = random.randint(1, W)
            graf[k][l], graf[l][k] = wys, wys
            dodatkowe_krawedzie -= 1
    return graf, nazwy

def los_nazwy(n):    
    nazwy_schronisk = ["Chatka", "Szrenica", "Strzecha", "Pasterka", "Kopa", "Puchatek", "Rycerz", "Halny", "Doktorek", "Profesorek",
                       "Rycerz", "Polanka", "Rysinka", "Sudetki", "Łysinka", "Domek", "Schron", "Czarownica", "Gzik", "Bigos",
                       "Piwko", "Słoneczne", "Pod chmurką", "Gwiazdka", "Milutkie", "Polanka", "Wrzosik", "Po drodze", "Tęczowe", "Tatrzańskie",
                       "Korona", "Burzowe", "Spadająca gwiazda", "Taterka", "Śnieżka", "Schron", "Wiedźma", "Zielone", "Niebieskie", "Srebrne",
                       "Przystanek", "Górka", "Wierch", "Wysokie", "Niżynka", "Kamyczek", "Na zakręcie", "Radosne", "Grota", "Słone",
                       "Zakręcone", "Piękne", "Koziczka", "Salamandra", "Koziołek", "Smaczne", "Przytulne", "Zacisze", "Cieplutkie", "Odpoczynek"]
    if n > len(nazwy_schronisk):
        return
    
    schroniska = random.sample(nazwy_schronisk, n)
    return schroniska

def osiagalne_wierzch(graf, maxW, start=0):
    n = len(graf)  # liczba wierzchołków
    odwiedzone = []
        
    def dfs(a):
        odwiedzone.append(a)
        for sasiad in range(n):
            if sasiad not in odwiedzone and graf[a][sasiad] != 0 and graf[a][sasiad] <= maxW:
                dfs(sasiad)
        
    dfs(start)
    return odwiedzone

def rys_graf(graf, nazwy=0):
    G = nx.from_numpy_array(np.array(graf))
    pos = nx.spring_layout(G)
    labels1 = nx.get_edge_attributes(G, 'weight')

    if nazwy == 0:
        nx.draw_networkx(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels1)

    else:
        labels2 = {i: nazwy[i] for i in range(len(nazwy))}
        nx.draw_networkx(G, pos, with_labels=False)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels1)
        nx.draw_networkx_labels(G, pos, labels=labels2, font_color="black")

    plt.show()

def main():
    graf, nazwy, Wmax, numer = dane()
    wynik = osiagalne_wierzch(graf, Wmax, numer)
    nazwy_osiagalnych = [(nazwy[indeks], indeks) for indeks in wynik]
    print('Zaczynając z wierzchołka', nazwy[numer], '(numer', numer, ')', 'profesor Bajtazar może dojść do wierzchołków:', nazwy_osiagalnych,
          'przy maksymalnej bezpiecznej wysokości =', Wmax)
    rys_graf(graf, nazwy)

if __name__ == "__main__":
    main()
