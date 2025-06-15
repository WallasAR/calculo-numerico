import os
from flask import Blueprint, render_template, request
from sympy import symbols, sympify, lambdify
from sympy.core.sympify import SympifyError

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
num_integration_bp = Blueprint(
    name='num-integration', 
    import_name=__name__, 
    url_prefix='/num-integration',
    template_folder=template_dir    
)

def trapeze(f, a, b, n):
    h = (b - a) / n
    x_points = [a + i * h for i in range(n + 1)]
    weights = [1] + [2] * (n - 1) + [1]
    fx = [f(xi) for xi in x_points]
    integral = (h / 2) * sum(w * y for w, y in zip(weights, fx))
    return integral, x_points, weights, fx

def simpson(f, a, b, n):
    if n % 2 != 0:
        return None, None, None, None
    h = (b - a) / n
    x_points = [a + i * h for i in range(n + 1)]
    weights = [1] + [4 if i % 2 == 1 else 2 for i in range(1, n)] + [1]
    fx = [f(xi) for xi in x_points]
    integral = (h / 3) * sum(w * y for w, y in zip(weights, fx))
    return integral, x_points, weights, fx

@num_integration_bp.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    pontos = []
    pesos = []
    valores = []
    metodo = ""
    tol = ""
    func_str = ""
    a = b = n = None

    if request.method == "POST":
        func_str = request.form.get("fx")
        a = float(request.form.get("a"))
        b = float(request.form.get("b"))
        n = int(request.form.get("n"))
        tol = float(request.form.get("tol"))
        x = symbols('x')
        try:
            expr = sympify(func_str)
            f = lambdify(x, expr, 'math')
        except SympifyError:
            error = "Função inválida!"
            return render_template("numerical_integration.html", result=result, error=error, pontos=pontos, pesos=pesos, valores=valores, metodo=metodo, fx=func_str, a=a, b=b, n=n, tol=tol)

        if n % 2 == 0:
            simpson_result = simpson(f, a, b, n)
            if simpson_result[0] is not None:
                integral_s, x_s, w_s, fx_s = simpson_result
                integral_s2, *_ = simpson(f, a, b, 2 * n)
                erro = abs(integral_s2 - integral_s) / 15 if integral_s2 is not None else None
                if erro is not None and erro < tol:
                    result = integral_s
                    pontos = x_s
                    pesos = w_s
                    valores = fx_s
                    metodo = "Simpson"
                    return render_template("numerical_integration.html", result=result, error=error, pontos=pontos, pesos=pesos, valores=valores, metodo=metodo, fx=func_str, a=a, b=b, n=n, tol=tol, erro_estimado=erro)
                else:
                    error = "Simpson não atingiu a tolerância desejada. Aplicando Trapézio como alternativa."
        if n % 2 != 0:
            error = "Simpson não pode ser aplicado (n deve ser par). Usando Trapézio."

        integral_t, x_t, w_t, fx_t = trapeze(f, a, b, n)
        result = integral_t
        pontos = x_t
        pesos = w_t
        valores = fx_t
        metodo = "Trapézio"
        return render_template("numerical_integration.html", result=result, error=error, pontos=pontos, pesos=pesos, valores=valores, metodo=metodo, fx=func_str, a=a, b=b, n=n, tol=tol)

    return render_template("numerical_integration.html", result=result, error=error, pontos=pontos, pesos=pesos, valores=valores, metodo=metodo, fx=func_str, a=a, b=b, n=n, tol=tol)