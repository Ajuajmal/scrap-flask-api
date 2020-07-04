from flask import Flask, request, jsonify,render_template
app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def respond():
    if request.method == 'POST':
        data = request.form['data']
        link = request.form['url']

        req = [{
            'link':link,
            'data':data,
        }]
        return jsonify(req)
    return render_template('api.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
