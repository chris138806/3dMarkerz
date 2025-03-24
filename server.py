from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

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

if __name__ == "__main__":
    app.run(debug=True)
