from flask import Flask, render_template, render_template_string, request

app = Flask(__name__) 

@app.route('/selectusername')
def selectusername_page():

    userlist = [['James'], ['Adam'], ['Mark']]

    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8">
<body>
<form action="/showusername">
    <button>Continue</button>
        <h1>Select User</h1>
<select id="currentuser" name="currentuser">
{% for user in userlist %}
  <option value="{{user[0]}}">{{user[0]}}</option>
{% endfor %}
</select>
</form>
</body>
</html>''', userlist=userlist)

@app.route('/showusername', methods=['POST', 'GET'])
def showusername_page():
    print('args:', request.args)
    print('form:', request.form)

    #currentuser = request.args.get("currentuser")
    currentuser = request.form.get("currentuser")

    return render_template_string('''<h1>Hello {{ currentuser }}</h1>''', currentuser=currentuser)

if __name__ == '__main__':
    app.run(debug=True)