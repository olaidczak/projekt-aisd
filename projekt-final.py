import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def dane():
    print("Witaj Podróżniku! Program pomoże ci wybrać schroniska do których możesz bezpiecznie dotrzeć podczas twojej wyprawy.")
    
    while True:
        try:
            wybor = int(input("Wybierz opcję: 1 - Podaj własne dane, 2 - Wygeneruj losowy graf: "))
            if wybor == 1:
                while True:
                    try:
                        n = int(input("Podaj liczbę schronisk: "))
                        if n <= 0:
                            raise ValueError("Liczba schronisk musi być dodatnia.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)
                
                while True:
                    try:
                        print("Podaj macierz nxn, symetryczną, z zerami na głównej przekątnej (odzwierciedlającą istnienie szlaków jako niezerowe liczby oraz ich wysokość jako wartość liczby) jako wiersze liczb oddzielonych spacjami (n x n):")
                        graf = []

                        for i in range(n):
                            while True:
                                try:
                                    wiersz = list(map(int, input(f"Wiersz {i+1}: ").split()))
                                    if len(wiersz) != n:
                                        raise ValueError(f"Wiersz musi zawierać {n} liczby.")
                                    graf.append(wiersz)
                                    break  
                                except ValueError as e:
                                    print("Błąd:", e)

                        for i in range(n):
                            for j in range(n):
                                if graf[i][j] != graf[j][i]:
                                    raise ValueError(f"Macierz musi być symetryczna!")

                            if graf[i][i] != 0:
                                raise ValueError(f"Wartość na przekątnej musi być zerem!")

                        break

                    except ValueError as e:
                        print("\nBłąd w macierzy:", e)
                        print("Spróbuj ponownie wprowadzić całą macierz.\n")
                nazwy = []
                print("Podaj nazwy schronisk (po jednej na wiersz):")
                for i in range(n):
                    nazwy.append(input(f"Nazwa dla wierzchołka {i+1}: "))

                while True:
                    try:
                        Wmax = int(input("Podaj maksymalną bezpieczną wysokość szlaku (Wmax): "))
                        if Wmax <= 0:
                            raise ValueError("Wysokość musi być liczbą dodatnią.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)
                
                while True:
                    try:
                        numer = int(input("Podaj numer wierzchołka startowego: "))
                        if numer < 0 or numer >= n:
                            raise ValueError(f"Numer wierzchołka startowego musi być >= 0 i < {n}.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)
                
                return graf, nazwy, Wmax, numer

            elif wybor == 2:
                while True:
                    try:
                        n = int(input("Podaj liczbę wierzchołków (n): "))
                        if n <= 0:
                            raise ValueError("Liczba wierzchołków musi być dodatnia.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)
                
                while True:
                    try:
                        m = int(input("Podaj liczbę krawędzi (m): "))
                        if m < n - 1:
                            raise ValueError("Graf będzie niespójny. Podaj liczbę >= n-1.")
                        if m > n * (n - 1) / 2:
                            raise ValueError("Za dużo krawędzi w grafie.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)

                while True:
                    try:
                        Wmax = int(input("Podaj maksymalną bezpieczną wysokość szlaku (Wmax): "))
                        if Wmax <= 0:
                            raise ValueError("Wysokość musi być liczbą dodatnią.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)

                while True:
                    try:
                        W = int(input("Podaj największą wysokość jaka ma być w grafie (W): "))
                        if W < Wmax:
                            raise ValueError("Wysokość W musi być większa lub równa Wmax.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)

                while True:
                    try:
                        numer = int(input("Podaj numer wierzchołka startowego: "))
                        if numer < 0 or numer >= n:
                            raise ValueError(f"Numer wierzchołka startowego musi być >= 0 i < {n}.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)

                graf, nazwy = los_graf(n, m, W)
                return graf, nazwy, Wmax, numer

            else:
                print("Nieprawidłowy wybór. Spróbuj ponownie.")
        except ValueError:
            print("Błąd: Złe dane.")


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
        return list(range(0,n))
    
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
        labels2 = {i: str(i) for i in range(len(graf))}
        nx.draw_networkx(G, pos, with_labels=False)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels1)
        nx.draw_networkx_labels(G, pos, labels=labels2, font_color="black")
    else:
        labels2 = {i: f"{nazwy[i]} ({i})" for i in range(len(nazwy))}
        nx.draw_networkx(G, pos, with_labels=False)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels1)
        nx.draw_networkx_labels(G, pos, labels=labels2, font_color="black")

    plt.show()

def main():
    while True:
        graf, nazwy, Wmax, numer = dane()
        
        while True:
            wynik = osiagalne_wierzch(graf, Wmax, numer)
            nazwy_osiagalnych = [(nazwy[indeks], indeks) for indeks in wynik]
            print('Zaczynając z wierzchołka', nazwy[numer], '(numer', numer, ')', 'profesor Bajtazar może dojść do wierzchołków:', nazwy_osiagalnych,
                  'przy maksymalnej bezpiecznej wysokości =', Wmax)
            print('UWAGA: Jeśli chcesz zacząć od innego wierzchołka lub wywołać program dla innego grafu zamknij okno z rysunkiem grafu.')
            rys_graf(graf, nazwy)

            zmien_start = input("Czy chcesz wystartować z innego wierzchołka? (tak/nie): ").lower()
            if zmien_start == 'tak':
                while True:
                    try:
                        numer = int(input(f"Podaj nowy numer wierzchołka startowego (0 do {len(graf)-1}): "))
                        if numer < 0 or numer >= len(graf):
                            raise ValueError(f"Numer wierzchołka startowego musi być >= 0 i < {len(graf)}.")
                        break
                    except ValueError as e:
                        print("Błąd:", e)
            else:
                break
            
        decyzja = input("Czy chcesz wywołać program dla innego grafu? (tak/nie): ").lower()
        if decyzja != 'tak':
            print("To był bardzo sportowy i obfitujący w krajobrazy dzień! Do zobaczenia, Podróżniku!")
            break

if __name__ == "__main__":
    main()
