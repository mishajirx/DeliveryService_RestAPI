from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



@app.route('/')
def hello():
    return 'Hello go Misha'

def main():
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
