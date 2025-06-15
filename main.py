from flask import Flask, render_template
from numerical_integration.app import num_integration_bp
from nonlinear_equations.app import nonlinear_bp
from newton_interpol.app import newton_interpol_bp

app = Flask(__name__)
app.register_blueprint(num_integration_bp)
app.register_blueprint(nonlinear_bp)
app.register_blueprint(newton_interpol_bp)

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)