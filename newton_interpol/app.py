from flask import Blueprint, render_template, request
import sympy as sp
import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
newton_interpol_bp = Blueprint(
    name='newton-interpol',
    import_name=__name__,
    url_prefix='/newton-interpol',
    template_folder=template_dir
)

def splitDifferences(pairs):
    n = len(pairs)
    x = [p[0] for p in pairs]
    y = [p[1] for p in pairs]

    table = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        table[i][0] = y[i]

    steps = []  # Lista dos passos LaTeX

    for j in range(1, n):
        for i in range(n - j):
            numerador = table[i+1][j-1] - table[i][j-1]
            denominador = x[i+j] - x[i]
            table[i][j] = numerador / denominador

            step_latex = (
                f"f[x_{{{i}}},\\dots,x_{{{i+j}}}] = "
                f"\\frac{{f[x_{{{i+1}}},\\dots,x_{{{i+j}}}] - f[x_{{{i}}},\\dots,x_{{{i+j-1}}}]}}{{x_{{{i+j}}} - x_{{{i}}}}} = "
                f"\\frac{{{sp.pretty(table[i+1][j-1])} - {sp.pretty(table[i][j-1])}}}{{{x[i+j]} - {x[i]}}} = {sp.pretty(table[i][j])}"
            )
            steps.append(step_latex)

    # Gerar LaTeX da tabela
    latex_table = "\\begin{array}{c|" + "c" * n + "}\n"
    latex_table += "x & f[x] & " + " & ".join([f"\\Delta^{i}f[x]" for i in range(1, n)]) + " \\\\\n\\hline\n"
    for i in range(n):
        latex_table += f"{x[i]}"
        for j in range(n - i):
            val = table[i][j]
            latex_table += f" & {sp.pretty(val)}"
        latex_table += " \\\\\n"
    latex_table += "\\end{array}"

    # Construir polinômio
    X = sp.Symbol('x')
    polynomial = table[0][0]
    terms = [f"{table[0][0]}"]
    product_term = 1
    for i in range(1, n):
        product_term *= (X - x[i - 1])
        term = table[0][i] * product_term
        polynomial += term
        terms.append(f"{sp.pretty(table[0][i])}·" + "".join([f"(x - {x[j]})" for j in range(i)]))

    latex_poly = "P(x) = " + " + ".join(terms)

    return sp.simplify(polynomial), latex_poly, latex_table, steps

def build_polynomial(table, x_vals):
    x = sp.symbols('x')
    n = len(x_vals)
    polynomial = table[0][0]
    term = 1
    for i in range(1, n):
        term *= (x - x_vals[i - 1])
        polynomial += table[i][0] * term
    return sp.simplify(polynomial)

def calc_polynomial(point, polyn_formula):
    x = sp.symbols('x')
    return polyn_formula.subs(x, point)

# Função utilitária
def parse_input(input_str):
    pairs_str = input_str.split("-")
    pairs = []
    for pair in pairs_str:
        x_str, y_str = pair.strip("() ").split(",")
        pairs.append((float(x_str), float(y_str)))
    return pairs

# Rota principal
@newton_interpol_bp.route('/', methods=['GET', 'POST'])
def index():
    result = None
    point = None
    value = None
    latex_poly = ""
    latex_table = ""
    steps = []
    
    if request.method == 'POST':
        try:
            raw_pairs = request.form['pairs']
            point = float(request.form['point'])
            pairs = [tuple(map(float, p.strip("() ").split(','))) for p in raw_pairs.split('-')]
            poly, latex_poly, latex_table, steps = splitDifferences(pairs)
            value = poly.subs('x', point)
            result = True
        except Exception as e:
            result = str(e)

    return render_template('newton_interpol.html',
                       result=result,
                       value=value,
                       latex_poly=latex_poly,
                       latex_table=latex_table,
                       point=point,
                       steps=steps)