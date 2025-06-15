# 🧮 Cálculo Numérico — Projetos Web Interativos

Este repositório reúne **três projetos web interativos** desenvolvidos como parte da disciplina de Cálculo Numérico. Cada projeto aborda um tema essencial da área:

- **Integração Numérica**  
- **Equações Não Lineares**  
- **Interpolação de Newton**

Todos os projetos compartilham uma **interface web moderna e responsiva**, construída com **Flask**, **Bootstrap** e **MathJax** para visualização de fórmulas em LaTeX. Eles rodam na mesma aplicação, com caminhos distintos.

---

## 🚀 Tecnologias Utilizadas

- 🐍 **Python 3**
- 🌐 **Flask** — Microframework Web
- 📐 **SymPy** — Cálculo simbólico
- 🎨 **Bootstrap 5** — Estilização responsiva
- 🧠 **MathJax** — Renderização LaTeX
- 🧩 **Jinja2** — Templates dinâmicos

---

## 🔧 Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/cálculo-numerico.git
   cd calculo-numerico
   ```

2. Instale as dependências:
   ```bash
   pip install flask sympy
   ```

3. Execute o servidor:
   ```bash
   python main.py
   ```

4. Acesse no navegador:  
   [`http://localhost:5000/`](http://localhost:5000/)

5. (Opcional) Você pode executar os projetos pelo terminal, dentro de cada pasta de projeto existe um arquivo chamado ```trabalho_cmd.py``` onde pode executar diretamente pelo termuinal.
---

## 🧩 Projetos Disponíveis

### 1. 🔢 Integração Numérica  
📍 Caminho: `/num-integration/`

**Descrição:**  
Permite calcular integrais definidas com os métodos **do Trapézio** e **de Simpson 1/3**, escolhendo automaticamente o mais adequado com base na entrada.

**Funcionalidades:**
- Entrada de função, intervalo `[a, b]`, número de subintervalos `n` e tolerância.
- Verificação se o método de Simpson é aplicável (`n` par e erro aceitável).
- Exibição dos pontos, pesos e valores de `f(x)`.
- Cálculo detalhado e resultado final.

---

### 2. ⚙️ Equações Não Lineares  
📍 Caminho: `/nonlinear/`

**Descrição:**  
Resolve equações não lineares com os métodos da **Bisseção**, **Newton-Raphson** e **Ponto Fixo**, exibindo passo a passo até a convergência.

**Funcionalidades:**
- Seleção do método.
- Entrada de função, valores iniciais e critério de parada.
- Validação automática dos dados (ex: sinais opostos para Bisseção).
- Exibição das iterações e do resultado final.

---

### 3. 📈 Interpolação de Newton  
📍 Caminho: `/newton-interpol/`

**Descrição:**  
Gera o polinômio interpolador de Newton com base em uma lista de pontos, exibindo a tabela de diferenças divididas e o polinômio resultante em LaTeX.

**Funcionalidades:**
- Entrada dos pares `(xi, yi)`.
- Cálculo das diferenças divididas.
- Construção simbólica do polinômio.
- Avaliação para um ponto escolhido.
- Visualização matemática detalhada com LaTeX.

---

## 🗂 Estrutura de Diretórios

```
calculo-numerico/
│
├── main.py                    # Arquivo principal (ponto de entrada)
├── templates/
│   └── home.html              # Menu principal
│
├── numerical_integration/
│   ├── app.py
│   ├── trabalho_cmd.py
│   └── templates/
│       └── numerical_integration.html
│
├── nonlinear_equations/
│   ├── app.py
│   ├── trabalho_cmd.py
│   └── templates/
│       └── nonlinear_equations.html
│
├── newton_interpol/
│   ├── app.py
│   ├── trabalho_cmd.py
│   └── templates/
│       └── newton_interpol.html
```

---

## 📚 Créditos e Licença

Este projeto foi desenvolvido com fins **educacionais**, na disciplina de **Cálculo Numérico**.  
Sinta-se livre para estudar, modificar e utilizar como quiser!

---