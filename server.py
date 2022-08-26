from flask import Flask

app = Flask(__name__)

@app.route('/api/stt', methods=['POST'])
def stt_controller():
    pass


def main():
    app.run(
        host='localhost',
        port=9999,
        debug=True
    )

if (__name__=='__main__'):
    main()
