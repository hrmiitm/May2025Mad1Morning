from flask import Flask, request, render_template # Flask == CLASS

app = Flask(__name__)# Its objec

# /
# /?
# /?id=50
# /?id=50&name=hritk&people=13
@app.route('/', methods=['GET'])
def asdhfasd():
    id = request.args.get('id')
    name = request.args.get('name')

    return render_template("home.html")

# /hello/anything/2323
# /hello/asdf/134
# /hello/anything/2h1           NotAllowed
# /hello                        NotAllowed
# /hello/anything               NotAllowed
# /hello/74                     NotAllowed
@app.route('/hello/<string:name>/<int:id>', methods=['GET'])
def hello_name(name, id):
    return f"Hello, {name}! Your ID is {id}."

app.run(debug=True)