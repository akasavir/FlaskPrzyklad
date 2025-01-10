from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "tajny_klucz"  # Klucz do szyfrowania sesji (musisz zmienić na coś trudnego)

# Inicjalizacja managera logowania
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Widok, na który użytkownik zostanie przekierowany, jeśli nie jest zalogowany

# Załóżmy, że mamy użytkownika o nazwie 'admin' i haśle '1234'
users = {"admin": {"password": "1234"}}

# Prosta klasa użytkownika (wymaga identyfikatora użytkownika)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Funkcja do ładowania użytkownika po ID (tutaj sprawdzamy, czy użytkownik istnieje w słowniku 'users')
@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/')
def home():
    return render_template('home.html')  # Strona główna

@app.route('/about')
def about():
    return render_template('about.html')  # Strona 'o nas'

@app.route('/faq')
def faq():
    return render_template('faq.html')  # Strona FAQ

# Logika dla strony logowania
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Jeśli użytkownik istnieje i hasło jest poprawne
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)  # Logowanie użytkownika
            flash("Zalogowano pomyślnie!", "success")  # Komunikat o sukcesie
            return redirect(url_for("dashboard"))  # Przekierowanie na stronę dashboard
        else:
            flash("Nieprawidłowe dane logowania.", "danger")  # Komunikat o błędzie
    return render_template("login.html")  # Strona logowania

# Strona chroniona (dostępna tylko po zalogowaniu)
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Witaj, {current_user.id}! To jest strona chroniona."  # Przykład strony, która jest dostępna tylko dla zalogowanych użytkowników

# Logowanie użytkownika (wylogowanie)
@app.route("/logout")
@login_required
def logout():
    logout_user()  # Wylogowanie użytkownika
    flash("Wylogowano pomyślnie!", "success")  # Komunikat o sukcesie
    return redirect(url_for("login"))  # Przekierowanie na stronę logowania

if __name__ == "__main__":
    app.run(debug=True)  # Uruchomienie aplikacji
