from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import smtplib
from email.message import EmailMessage

# Configurazione email per Register.it
EMAIL_ADDRESS = "preventivi@3dmarkerz.it"  # Email mittente su Register.it
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Password sicura da variabile ambiente
SMTP_SERVER = "authsmtp.securemail.pro"
SMTP_PORT = 465  # Porta SSL

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Permetti a Flask di servire i file STL
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summary")
def summary():
    filename = request.args.get("filename")
    print_type = request.args.get("print_type", "Non specificato")
    resina_color = request.args.get("resina_color", "N/A")
    resina_infill = request.args.get("resina_infill", "N/A")
    filo_material = request.args.get("filo_material", "N/A")
    filo_quality = request.args.get("filo_quality", "N/A")
    filo_color = request.args.get("filo_color", "N/A")
    filo_infill = request.args.get("filo_infill", "N/A")

    return render_template(
        "summary.html", filename=filename, print_type=print_type,
        resina_color=resina_color, resina_infill=resina_infill,
        filo_material=filo_material, filo_quality=filo_quality,
        filo_color=filo_color, filo_infill=filo_infill
    )

@app.route("/contatti")
def contatti():
    return render_template("contatti.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Errore: Nessun file selezionato."

    file = request.files["file"]
    if file.filename == "":
        return "Errore: Nessun file selezionato."

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    print(f"✅ File caricato: {file.filename}, redirecting to summary...")

    return redirect(url_for("summary", filename=file.filename, print_type=request.form.get("print_type", ""),
                            resina_color=request.form.get("resina_color", ""),
                            resina_infill=request.form.get("resina_infill", ""),
                            filo_material=request.form.get("filo_material", ""),
                            filo_quality=request.form.get("filo_quality", ""),
                            filo_color=request.form.get("filo_color", ""),
                            filo_infill=request.form.get("filo_infill", "")))

@app.route("/send-email", methods=["POST"])
def send_email():
    email = request.form["email"]
    notes = request.form["notes"]
    filename = request.form["filename"]
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    print_type = request.form.get("print_type", "N/A")
    resina_color = request.form.get("resina_color", "N/A")
    resina_infill = request.form.get("resina_infill", "N/A")
    filo_material = request.form.get("filo_material", "N/A")
    filo_quality = request.form.get("filo_quality", "N/A")
    filo_color = request.form.get("filo_color", "N/A")
    filo_infill = request.form.get("filo_infill", "N/A")

    file_url = url_for('uploaded_file', filename=filename, _external=True)

    messaggio = f"""
Nuova richiesta di preventivo:

- Email cliente: {email}
- File caricato: {filename}
- Tipo di stampa: {print_type}
"""

    if print_type == "resina":
        messaggio += f"- Colore Resina: {resina_color}\n- Riempimento Resina: {resina_infill}\n"
    elif print_type == "filo":
        messaggio += f"- Materiale Filo: {filo_material}\n- Qualità: {filo_quality}\n- Colore: {filo_color}\n- Riempimento: {filo_infill}\n"

    messaggio += f"- Note aggiuntive: {notes}\n"
    messaggio += f"- Link per scaricare il file: {file_url}\n"

    try:
        msg = EmailMessage()
        msg["Subject"] = "RICHIESTA NUOVO PREVENTIVO DI STAMPA"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = "info@3dmarkerz.it"
        msg.set_content(messaggio)

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        return "Email inviata con successo!"
    except Exception as e:
        print(f"Errore invio email: {e}")
        return "Errore durante l'invio dell'email."

if __name__ == "__main__":
    app.run(debug=True)