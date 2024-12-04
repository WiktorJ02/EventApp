from app import create_app, db
from flask import Flask

app = create_app('dev')

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'app': app}

if __name__ == "__main__":
    app.run()
