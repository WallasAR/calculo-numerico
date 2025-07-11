import os
from flask import Blueprint, render_template, request
from sympy import symbols, sympify, lambdify, diff
from sympy.core.sympify import SympifyError

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
nonlinear_bp = Blueprint(
    name='nonlinear', 
    import_name=__name__, 
    url_prefix='/nonlinear',
    template_folder=template_dir
)

def bisection(function, a, b, epsilon):
    x = symbols('x')
    try:
        expr = sympify(function)
        f = lambdify(x, expr, 'math')
    except SympifyError:
        return None, [], "Função inválida", None, None, 0, None

    info = None
    if a > b:
        a, b = b, a
        info = "Os valores de a e b foram trocados para manter a < b."

    steps = []
    iter_count = 0

    # Protege a avaliação de f(a) e f(b)
    try:
        fa = f(a)
        fb = f(b)
    except Exception as e:
        return None, [], f"Erro ao avaliar f(a) ou f(b): {e}", None, None, 0, info

    if fa * fb >= 0:
        return None, [], "Os extremos não têm sinais opostos", None, None, 0, info

    c = (a + b) / 2.0
    while (b - a) / 2.0 > epsilon:
        c = (a + b) / 2.0
        try:
            fc = f(c)
        except Exception as e:
            return None, steps, f"Erro ao avaliar f(c): {e}", a, b, iter_count, info
        steps.append(f"a_{iter_count} = {a:.6f}, b_{iter_count} = {b:.6f}, x_{iter_count} = {c:.6f}, f(x_{iter_count}) = {fc:.6f}")
        if fc == 0:
            break
        elif fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        iter_count += 1
    return c, steps, None, a, b, iter_count, info

def newton_raphson(function, x0, epsilon):
    x = symbols('x')
    try:
        expr = sympify(function)
        f = lambdify(x, expr, 'math')
        f_prime = lambdify(x, diff(expr, x), 'math')
    except SympifyError:
        return None, [], "Função inválida", 0
    steps = []
    iter_count = 0
    erro = float('inf')
    max_iter = 1000
    while erro > epsilon and iter_count < max_iter:
        try:
            fx = f(x0)
            fpx = f_prime(x0)
        except ValueError as e:
            return None, steps, f"Erro de domínio matemático: {e}", iter_count
        if fpx == 0:
            return None, steps, "Derivada igual a zero", iter_count
        x1 = x0 - fx / fpx
        erro = abs(x1 - x0)
        steps.append(f"x_{iter_count} = {x0:.6f}, f(x_{iter_count}) = {fx:.6f}, f'(x_{iter_count}) = {fpx:.6f}, erro = {erro:.6f}")
        x0 = x1
        iter_count += 1
    return x0, steps, None, iter_count

def fixed_point(func_fx, func_gx, x0, epsilon):
    x = symbols('x')
    try:
        expr_f = sympify(func_fx)
        expr_g = sympify(func_gx)
        if expr_f is None or expr_g is None:
            return None, [], "Função inválida", 0
        f = lambdify(x, expr_f, 'math')
        g = lambdify(x, expr_g, 'math')
    except (SympifyError, TypeError) as e:
        return None, [], f"Erro ao interpretar funções: {e}", 0
    steps = []
    iter_count = 0
    erro = float('inf')
    max_iter = 1000
    while erro > epsilon and iter_count < max_iter:
        try:
            x1 = g(x0)
            fx1 = f(x1)
            erro = abs(x1 - x0)
        except Exception as e:
            return None, steps, f"Erro durante a iteração: {e}", iter_count
        steps.append(f"x_{iter_count} = {x0:.6f}, g(x_{iter_count}) = {x1:.6f}, f(x_{iter_count}) = {fx1:.6f}, erro = {erro:.6f}")
        x0 = x1
        iter_count += 1
    return x0, steps, None, iter_count

@nonlinear_bp.route("/", methods=["GET", "POST"])
def index():
    method = request.args.get("method", "bissecao")
    result = None
    steps = []
    error = None
    a_final = b_final = None
    info = None

    if request.method == "POST":
        method = request.form.get("metodo", "bissecao")
        tol = float(request.form.get("tol", "0.01"))
        if method == "bissecao":
            fx = request.form.get("fx")
            a = float(request.form.get("a"))
            b = float(request.form.get("b"))
            root, steps, error, a_final, b_final, iterations, info = bisection(fx, a, b, tol)
            if not error:
                result = {"root": f"{root:.6f}", "iterations": iterations}
        elif method == "newton":
            fx = request.form.get("fx")
            x0 = float(request.form.get("x0"))
            root, steps, error, iterations = newton_raphson(fx, x0, tol)
            if not error:
                result = {"root": f"{root:.6f}", "iterations": iterations}
        elif method == "ponto_fixo":
            func_fx = request.form.get("fx")
            func_gx = request.form.get("func_gx")
            x0 = float(request.form.get("x0"))
            root, steps, error, iterations = fixed_point(func_fx, func_gx, x0, tol)
            if not error:
                result = {"root": f"{root:.6f}", "iterations": iterations}
        else:
            error = "Método não implementado"

        return render_template(
            "nonlinear_equations.html",
            method=method,
            result=result,
            steps=steps,
            error=error,
            info=info,
            fx=request.form.get("fx"),
            func_fx=request.form.get("fx"),
            func_gx=request.form.get("func_gx"),
            a=request.form.get("a"),
            b=request.form.get("b"),
            x0=request.form.get("x0"),
            tol=request.form.get("tol"),
            a_final=a_final,
            b_final=b_final,
        )

    return render_template("nonlinear_equations.html", method=method, result=None, steps=[])