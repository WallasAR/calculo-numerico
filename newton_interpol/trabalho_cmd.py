from sympy import symbols, simplify, expand

# Função que constrói a tabela de diferenças divididas
def splitDifferences(pairs):
    # Quantidade de pontos
    n = len(pairs)         
    
    # lista de valores (pares separados)
    x = [p[0] for p in pairs]        
    y = [p[1] for p in pairs]

    # Inicializa a tabela com a primeira coluna (valores de y)
    table = [y.copy()]                      

    # Calcula as diferenças divididas de ordem 1 até n-1
    for level in range(1, n):
        col = []
        for i in range(n - level):
            num = table[level - 1][i + 1] - table[level - 1][i]  # Numerador: diferença anterior
            den = x[i + level] - x[i]                            # Denominador: diferença de x
            col.append(num / den) 
        table.append(col) 
    
    return table, x

# Constrói o polinômio de Newton baseado na tabela
def build_polynomial(table, x_vals):
    x = symbols('x')  
    n = len(x_vals)
    
    # Começa com f[x0]
    polynomial = table[0][0]           
    # Termo acumulado (x - x0)(x - x1)...     
    term = 1                             
    for i in range(1, n):
        term *= (x - x_vals[i - 1])         # Multiplica o termo acumulado por (x - xi)
        polynomial += table[i][0] * term    # Soma o novo termo ao polinômio
    return simplify(polynomial)   

# Avalia o polinômio em um ponto
def calc_polynomial(point, polyn_formula):
    x = symbols('x')
    return polyn_formula.subs(x, point)     # Substitui x pelo valor desejado

# Mostra a tabela de diferenças no terminal
def format_table(table):
    print("\n📊 Tabela de Diferenças Divididas:")
    for i, row in enumerate(table):
        print(f"Ordem {i}: {['{:.4f}'.format(val) for val in row]}")

# Lê e transforma a string de entrada em uma lista de pares
def parse_input(input_str):
    pairs_str = input_str.split("),")                  # Separa os pares por "-"
    pairs = []
    for pair in pairs_str:
        x_str, y_str = pair.strip("() ").split(",")   # Remove () e espaços, separa por vírgula
        pairs.append((float(x_str), float(y_str)))    # Adiciona o par convertido pra float
    return pairs

def main():
    input_str = input("Digite a lista de pares (formato: (x1,y1),(x2,y2),...): ")
    point_polynomial = float(input("Digite um ponto desejado para calcular o polinômio: "))

    pairs = parse_input(input_str)                 
    table, x_vals = splitDifferences(pairs)  
    format_table(table)   

    polynomial = build_polynomial(table, x_vals)  
    print(f"\n📐 Polinômio de Newton (expandido):\nP(x) = {expand(polynomial)}")

    value = calc_polynomial(point_polynomial, polynomial)
    print(f"\n📍 P({point_polynomial}) = {value.evalf()}")

if __name__ == "__main__":
    main()
