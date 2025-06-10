import curses
from sympy import symbols, sympify, lambdify, init_printing
from sympy.core.sympify import SympifyError

def selectMethod(stdscr):
  # Initialize colors 
  curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Highlighted
  curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK) # Normal
  
  options = ["Bisseção", "Newton-Raphson", "Ponto Fixo"]
  current_selection = 0;
  
  while True:
    stdscr.clear()
    stdscr.addstr("Escolha o método de resolução: \n")
    
    for i, option in enumerate(options):
      if i == current_selection:
        stdscr.attron(curses.color_pair(1)) # Apply highlight
        stdscr.addstr(f"> {option}\n")
        stdscr.attroff(curses.color_pair(1))
      else:
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(f" {option}\n")
        stdscr.attroff(curses.color_pair(2))
        
    key = stdscr.getch()

    if key == curses.KEY_UP:
      current_selection = max(0, current_selection - 1)
    elif key == curses.KEY_DOWN:
      current_selection = min(len(options) - 1, current_selection + 1)
    elif key == curses.KEY_ENTER or key in [10, 13]: # Enter key
      stdscr.clear()
      return current_selection
      # stdscr.addstr(f"You selected: {options[current_selection]}\n")
      # stdscr.addstr("Press any key to continue...")
      # stdscr.getch()

def input_processing(function, params):
  x = symbols('x')

  try:
    expr = sympify(function)          # Converte string pra expressão
    f = lambdify(x, expr, 'math')         # Transforma pra função operavel 
  except SympifyError as e:
    print("Função inválida!")
    print(f"Erro: {e}")
    return

  try:
    a = float(params.split(",")[0])
    b = float(params.split(",")[1])
  except:
    print("Parâmetros iniciais inválidos. Digite como: 1,2")
    return

  if f(a) * f(b) >= 0:
    print("Os extremos não têm sinais opostos, não serve pra bisseção não!")
    return
  
  return a, b, f

def bisection(function, params, epsilon):
  a, b, f = input_processing(function, params)
  
  print("\nIter |     a     |     b     |     x     |   f(x)   ")
  print("-----+-----------+-----------+-----------+-----------")

  iter_count = 0
  c = (a + b) / 2.0
  while (b - a) / 2.0 > epsilon:
    c = (a + b) / 2.0
    fc = f(c)
    print(f"{iter_count:>4} | {a:>9.5f} | {b:>9.5f} | {c:>9.5f} | {fc:>9.5f}")
    if fc == 0:
      break
    elif f(a) * fc < 0:
      b = c
    else:
      a = c
    iter_count += 1

  print(f"x̄ ≈ {c:.4f} com ε = {epsilon}")

def fixed_point(func_fx, func_gx, epsilon, x0):
    x = symbols('x')

    try:
        expr_f = sympify(func_fx)
        expr_g = sympify(func_gx)
        f = lambdify(x, expr_f, 'math')
        g = lambdify(x, expr_g, 'math')
    except SympifyError as e:
        print("Erro ao interpretar funções.")
        print(f"Erro: {e}")
        return

    print("\nIter |     x_n     |   g(x_n)    |  f(x_n)   | Erro Abs.")
    print("-----+-------------+-------------+-----------+-----------")

    iter_count = 0
    max_iter = 1000
    erro = float('inf')

    while erro > epsilon and iter_count < max_iter:
      x1 = g(x0)
      fx1 = f(x1)
      erro = abs(x1 - x0)

      print(f"{iter_count:>4} | {x0:>11.6f} | {x1:>11.6f} | {fx1:>9.6f} | {erro:>9.6f}")
      x0 = x1
      iter_count += 1
        
    print(f"x̄ ≈ {x0:.4f} com ε = {epsilon}")


def newton_raphson(function, epsilon, init_value):
  from sympy import diff, symbols, lambdify, sympify

  x = symbols('x')

  try:
    expr = sympify(function)
    f = lambdify(x, expr, 'math')
    f_prime = lambdify(x, diff(expr, x), 'math')  # Derivada da função
  except SympifyError as e:
    print("Erro ao interpretar a função.")
    print(f"Erro: {e}")
    return

  try:
    x0 = float(init_value)
  except:
    print("Parâmetro inicial inválido. Digite como: 2")
    return

  print("\nIter |     x_n     |   f(x_n)    | f'(x_n)    | Erro Abs.")
  print("-----+-------------+-------------+------------+-----------")

  iter_count = 0
  max_iter = 1000
  erro = float('inf')

  while erro > epsilon and iter_count < max_iter:
    fx = f(x0)
    fpx = f_prime(x0)

    if fpx == 0:
      print("Derivada igual a zero. Método travou, man.")
      return

    x1 = x0 - fx / fpx
    erro = abs(x1 - x0)

    print(f"{iter_count:>4} | {x0:>11.6f} | {fx:>11.6f} | {fpx:>10.6f} | {erro:>9.6f}")
    x0 = x1
    iter_count += 1

  print(f"x̄ ≈ {x0:.4f} com ε = {epsilon}")

def main():
    init_printing()
    method = curses.wrapper(selectMethod)

    function = input("Digite a função (ex: x**3 - x - 2): ")
    epsilon = float(input("Digite o critério de parada (ex: 0.001): "))

    if method == 0: 
      params = input("Digite os parâmetros iniciais (a,b): ")
      bisection(function, params, epsilon)
    elif (method == 1):
      init_value = float(input("Digite o valor inicial da iteração: "))
      newton_raphson(function, epsilon, init_value)
    elif (method == 2):
      function_g = input("Digite a função g(x) (ex: (x+2)**(1/3)): ")
      init_value = float(input("Digite o valor inicial da iteração: "))
      fixed_point(function, function_g, epsilon, init_value)

if __name__ == "__main__":
  main()