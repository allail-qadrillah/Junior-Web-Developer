from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Membuat/mengkoneksikan database
    with app.app_context():
        db.create_all()

    # Menjalankan aplikasi
    app.run(debug=False)