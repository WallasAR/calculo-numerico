from sympy import symbols, sympify, lambdify
from sympy.core.sympify import SympifyError

# Função para o método do Trapézio
def trapeze(f, a, b, n):
    h = (b - a) / n  # Calcula o tamanho do subintervalo
    x_points = [a + i * h for i in range(n + 1)]  # Pontos de avaliação
    weights = [1] + [2] * (n - 1) + [1]  # Pesos do método do trapézio
    fx = [f(xi) for xi in x_points]  # Avaliação da função em cada ponto
    
    # Soma ponderada dos valores, multiplicada pelo tamanho do subintervalo
    integral = (h / 2) * sum(w * y for w, y in zip(weights, fx))
    return integral, x_points, weights, fx

# Função para o método de Simpson 1/3
def simpson(f, a, b, n):
    if n % 2 != 0:
        # Simpson só funciona para n par
        return None, None, None, None
    h = (b - a) / n  # Tamanho do subintervalo
    x_points = [a + i * h for i in range(n + 1)]  # Pontos de avaliação
    # Pesos: 1 nas extremidades, 4 nos ímpares, 2 nos pares (exceto extremos)
    weights = [1] + [4 if i % 2 == 1 else 2 for i in range(1, n)] + [1]
    fx = [f(xi) for xi in x_points]  # Avaliação da função em cada ponto
    
    # Soma ponderada dos valores, multiplicada pelo tamanho do subintervalo
    integral = (h / 3) * sum(w * y for w, y in zip(weights, fx))
    return integral, x_points, weights, fx

def main():
    func_str = input("Digite a função a ser integrada (ex: x**2 + 1): ")
    a = float(input("Limite inferior a: "))
    b = float(input("Limite superior b: "))
    n = int(input("Número de subintervalos n: "))
    tol = float(input("Tolerância desejada (ex: 0.001): "))

    x = symbols('x')
    try:
        # Converte a string para expressão simbólica e depois para função numérica
        expr = sympify(func_str)
        f = lambdify(x, expr, 'math')
    except SympifyError:
        print("Função inválida!")
        return

    simpson_result = None
    # Tenta aplicar Simpson se n for par
    if n % 2 == 0:
        simpson_result = simpson(f, a, b, n)
        if simpson_result[0] is not None:
            integral_s, x_s, w_s, fx_s = simpson_result
            # Calcula a integral novamente com o dobro de subintervalos para estimar o erro
            integral_s2, *_ = simpson(f, a, b, 2 * n)
            erro = abs(integral_s2 - integral_s) / 15 if integral_s2 is not None else None
            if erro is not None and erro < tol:
                # Se o erro for menor que a tolerância, aceita o resultado de Simpson
                print("\nMétodo de Simpson aplicado com sucesso!")
                print(f"Pontos de avaliação: {x_s}")
                print(f"Pesos: {w_s}")
                print(f"f(x) em cada ponto: {fx_s}")
                print(f"Valor da integral ≈ {integral_s:.6f}")
                print(f"Erro estimado: {erro:.6g} < tolerância {tol}")
                print("Método utilizado: Simpson")
                return
            else:
                # Se o erro for maior que a tolerância, avisa e usa Trapézio
                print("Simpson não atingiu a tolerância desejada. Aplicando Trapézio como alternativa.")

    # Se n for ímpar, Simpson não pode ser usado
    if n % 2 != 0:
        print("Simpson não pode ser aplicado (n deve ser par). Usando Trapézio.")

    # Aplica o método do Trapézio
    integral_t, x_t, w_t, fx_t = trapeze(f, a, b, n)
    print("\nMétodo do Trapézio")
    print(f"Pontos de avaliação: {x_t}")
    print(f"Pesos: {w_t}")
    print(f"f(x) em cada ponto: {fx_t}")
    print(f"Valor da integral ≈ {integral_t:.6f}")
    print("Método utilizado: Trapézio")

if __name__ == "__main__":
    main()