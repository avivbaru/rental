from flask import Flask, render_template, json, request, redirect
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from flask import session
import uuid
import os

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['UPLOAD_FOLDER'] = 'static/Uploads'

mysql.init_app(app)

pageLimit = 6



@app.route('/getAllRequests')
def getAllRequests():
    try:
        if session.get('user'):
             
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetAllRequests')
            result = cursor.fetchall()
         
 
         
            wishes_dict = []
            for wish in result:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'FilePath': wish[3],
                        'Price': wish[5]}
                wishes_dict.append(wish_dict)       
 
            
 
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/getAllOffers')
def getAllOffers():
    try:
        if session.get('user'):
             
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetAllOffers')
            result = cursor.fetchall()
         
 
         
            wishes_dict = []
            for wish in result:
                wish_dict = {
                        'Id': wish[0],
                        'Title': wish[1],
                        'Description': wish[2],
                        'FilePath': wish[3],
                        'Price': wish[5]}
                wishes_dict.append(wish_dict)       
 
            
 
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/showDashboard')
def showDashboard():
    return render_template('dashboard.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        extension = file.filename.split(".")[-1]
        f_name = str(uuid.uuid4()) + "." + extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
        return json.dumps({'filename':f_name})


@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteWish',(_id,_user))
            result = cursor.fetchall()
 
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/updateWish', methods=['POST'])
def updateWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            _title = request.form['title']
            _description = request.form['description']
            _price = request.form['price']
            _wish_id = request.form['id']
            _filePath = request.form['filePath']
            _isOffer = request.form['isOffer']
            _isDone = request.form['isDone']
 
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_updateWish',(_title,_description,_wish_id,_user,_filePath,_price,_isOffer,_isDone))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'ERROR'})
    except Exception as e:
        return json.dumps({'status':'Unauthorized access'})
    finally:
        cursor.close()
        conn.close()


@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        if session.get('user'):
 
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetWishById',(_id,_user))
            result = cursor.fetchall()
            wish = []
            wish.append({'Id':result[0][0],
                'Title':result[0][1],
                'Description':result[0][2],
                'FilePath':result[0][3],
                'isOffer': result[0][4],
                'Price': result[0][5],
                'Done':result[0][6]})
 
            return json.dumps(wish)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))


@app.route('/getWish',methods=['POST'])
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            _limit = pageLimit
            _offset = request.form['offset']
            _total_records = 0

            # Connect to MySQL and fetch data
            con = mysql.connect()
            cursor = con.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,_limit,_offset,_total_records))
            wishes = cursor.fetchall()

            cursor.close()

            cursor = con.cursor()
            cursor.execute('SELECT @_sp_GetWishByUser_3');

            outParam = cursor.fetchall()

 
            response = []
            wishes_dict = []
            
            for wish in wishes:
                wish_dict = {
                    'Id': wish[0],
                    'Title': wish[1],
                    'Description': wish[2],
                    'FilePath':wish[3],
                    'isOffer': wish[4],
                    'Price': wish[5],
                    'Done':wish[6]}

                wishes_dict.append(wish_dict)

            response.append(wishes_dict)
            response.append({'total':outParam[0][0]}) 
 
            return json.dumps(response)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))


@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _price = request.form['inputPrice']
            _user = session.get('user')
            _isoffer = 1 if bool(request.form.get('isoffer', "False")) else 0
            _filePath = request.form.get('filePath', '')
            _done = 1 if request.form.get('done') else 0

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addWish',(_title,_description,_user,_filePath,_isoffer,_price))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()                   
    

@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')

@app.route('/showSignUp')
def SignUpPage():
    return render_template('signup.html')


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')    


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            # still not working, the max length of columm password is not enouth
            if check_password_hash(str(data[0][3]),str(_password)):
                session['user'] = data[0][0]
                return redirect('/showDashboard')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.1')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/signUp',methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    if _name and _email and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        _hashed_password = generate_password_hash(_password)
        print _hashed_password
        print _password
        cursor.callproc('sp_createUser',(_name,_email,_hashed_password))

        data = cursor.fetchall()
 
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})

        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})        


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/userHome')
def userHome():    
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


if __name__ == "__main__":
    app.run()