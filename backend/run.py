from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

else:
    # Isso é necessário para o gunicorn/vercel encontrar o app
    application = app  # Renomeia para 'application' (padrão WSGI)