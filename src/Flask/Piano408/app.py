from flask import Flask
from flask_cors import CORS
from flask import request
from flask import send_file
import io

import tempfile
import csv
from flask import jsonify
import jsonify
import json
from flaskext.mysql import MySQL
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
CORS(app)
mysql = MySQL()
#connect to db here
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
"""
cursor.execute("SELECT * from Login")
data = cursor.fetchone()
print(data)
"""
#cursor.execute("INSERT INTO CompletedKeys(UserID,AMajorCompleted,BMAJORCOMPLETED,CMAJORCOMPLETED,DMAJORCOMPLETED,EMAJORCOMPLETED,FMAJORCOMPLETED,GMAJORCOMPLETED) VALUES (1,0,0,0,0,0,0,0)")
conn.commit()


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print(request.data)
    print(request.form.get("username"))
    print(request.form.get("password"))

    return 'hello world'

@app.route('/getScaleStart',methods = ['POST'])
def scaleStart():
    theKey = request.json["selectedScale"]
    majorMinor = request.json["isMajor"]
    if majorMinor == True:
        majorMinor = " Major"
    else:
        majorMinor = " Minor"


    selectScaleQuery = "SELECT Tonic FROM `Key` WHERE KeyName=" + repr(theKey + majorMinor)
    print(selectScaleQuery)
    cursor.execute(selectScaleQuery)
    startNum = cursor.fetchone()
    print(startNum)
    conn.commit()
    return str(startNum)
@app.route('/updatekeys/<uid>', methods=['POST'])
def update_keys(uid):
    if request.headers["Content-Type"] == "application/json":
        print(request.json["currentKeys"])
        return "ok"
    else:
        theKey = (request.json["currentKeys"])
        if theKey == "CMajor":
            keyAttribute = "CMajorCompleted"
        elif theKey == "GMajor":
            keyAttribute = "GMajorCompleted"
        elif theKey == "DMajor":
            keyAttribute = "DMajorCompleted"
        elif theKey == "AMajor":
            keyAttribute = "AMajorCompleted"
        elif theKey == "EMajor":
            keyAttribute = "EMajorCompleted"
        elif theKey == "BMajor":
            keyAttribute = "BMajorCompleted"
        elif theKey == "G♭Major":
            keyAttribute = "GFlatMajorCompleted"
        elif theKey == "D♭Major":
            keyAttribute = "DFlatMajorCompleted"
        elif theKey == "A♭Major":
            keyAttribute = "AFlatMajorCompleted"
        elif theKey == "E♭Major":
            keyAttribute = "EFlatMajorCompleted"
        elif theKey == "B♭Major":
            keyAttribute = "BFlatMajorCompleted"
        elif theKey == "FMajor":
            keyAttribute = "FMajorCompleted"
        elif theKey == "AMinor":
            keyAttribute = "AMinorCompleted"
        elif theKey == "EMinor":
            keyAttribute = "EMinorCompleted"
        elif theKey == "BMinor":
            keyAttribute = "BMinorCompleted"
        elif theKey == "F#Minor":
            keyAttribute = "FSharpMinorCompleted"
        elif theKey == "C#Minor":
            keyAttribute = "CSharpMinorCompleted"
        elif theKey == "G#Minor":
            keyAttribute = "GSharpMinorCompleted"
        elif theKey == "D#Minor":
            keyAttribute = "DSharpMinorCompleted"
        elif theKey == "A#Minor":
            keyAttribute = "ASharpMinorCompleted"
        elif theKey == "FMinor":
            keyAttribute = "FMinorCompleted"
        elif theKey == "CMinor":
            keyAttribute = "CMinorCompleted"
        elif theKey == "GMinor":
            keyAttribute = "GMinorCompleted"
        elif theKey == "DMinor":
            keyAttribute = "DMinorCompleted"

        updateKeyQuery = "UPDATE CompletedKeys SET " + keyAttribute + " = NOT " + keyAttribute + " WHERE UserID=" +uid  #need to incorporate uid
        cursor.execute(updateKeyQuery)

        conn.commit()
        return "not ok"


    conn.commit()
    return "ok"

def mapCompletesDict(completes): #create dictionary with key names and if key is complete
    mapped = {}
    keyType = "Major"
    for count,i in enumerate(completes):
        if count == 12:
            keyType = "Minor"
        if count == 7:
            mapped[chr(ord('A')) + "♭" + keyType] = i
        elif count == 8:
            mapped[chr(ord('B')) + "♭" + keyType] = i
        elif count == 9:
            mapped[chr(ord('D')) + "♭" + keyType] = i
        elif count == 10:
            mapped[chr(ord('E')) + "♭" + keyType] = i
        elif count == 11:
            mapped[chr(ord('G')) + "♭" + keyType] = i
        elif count == 19:
            mapped[chr(ord('A')) + "#" + keyType] = i
        elif count == 20:
            mapped[chr(ord('C')) + "#" + keyType] = i
        elif count == 21:
            mapped[chr(ord('D')) + "#" + keyType] = i
        elif count == 22:
            mapped[chr(ord('F')) + "#" + keyType] = i
        elif count == 23:
            mapped[chr(ord('G')) + "#" + keyType] = i
        else:
            if keyType == "Minor":
                mapped[chr(ord('A') + count-12) + keyType] = i
            else:
                mapped[chr(ord('A') + count) + keyType] = i
    print(mapped)
    return mapped


@app.route('/selectPieces/<uid>', methods=['GET'])
def selectPieces(uid):
    print(uid)

    piecesQuery = "SELECT Piece,Composer,Status FROM Pieces WHERE UserID = {}".format(uid)
    cursor.execute(piecesQuery)
    data = cursor.fetchall()

    piecesL = [j for j in data]
    return json.dumps(piecesL)

@app.route('/createUser', methods=['POST'])
def insert_user():
    username = request.json["username"]
    passwd = request.json["password"]

    insertUserQuery = "INSERT INTO Login(Username,Password) VALUES('{}','{}') ".format(username,passwd)
    try:
        cursor.execute(insertUserQuery)
        conn.commit()
        return "good"
    except:
        return "Username exists"

@app.route('/getUser', methods=['POST'])
def get_user():
    try:
        username = request.json["username"]
        print(username)
        passwd = request.json["password"]
        print(type(username))
        userQuery = "SELECT UserID,Password FROM Login WHERE Username='{}' AND isDeleted=0".format(username)
        cursor.execute(userQuery)
        userData = cursor.fetchall()
        print(userData)
        id = userData[0][0]
        corrPass = userData[0][1]
        if (corrPass == passwd):
            if (id) == 1:
                isAdmin = True
            else:
                isAdmin = False
            userDict = {"userID": id, "isAdmin": isAdmin}
            print(userDict)
            return json.dumps(userDict)
    except:
        return "bad"


    else:
        return "bad"



@app.route('/insertPieces', methods=['POST'])
def insertPieces():
    uID = request.json["userID"]
    piece = request.json["piece"]
    composer = request.json["composer"]
    status = request.json["status"]
    insertPiecesQuery = ("INSERT INTO Pieces VALUES({},'{}','{}','{}')").format(uID,piece,composer,status)
    cursor.execute(insertPiecesQuery)
    conn.commit()
    return "ok"


@app.route('/selectkeys', methods=['GET'])
def get_keys():
    # SELECT ALL ENTRIES THAT HAVE KEY COMPLETED... will have to check user ID later
    cursor.execute("SELECT AMajorCompleted, BMajorCompleted, CMajorCompleted,DMajorCompleted,EMajorCompleted,"
                   "FMajorCompleted,GMajorCompleted, BFlatMajorCompleted, EFlatMajorCompleted, AFlatMajorCompleted,"
                   "DFlatMajorCompleted, GFlatMajorCompleted, AMinorCompleted,BMinorCompleted, CMinorCompleted,"
                   "DMinorCompleted, EMinorCompleted, FMinorCompleted, GMinorCompleted, ASharpMinorCompleted, "
                   "CSharpMinorCompleted, DSharpMinorCompleted, FSharpMinorCompleted, GSharpMinorCompleted"
                   " FROM CompletedKeys WHERE UserID = 1")
    data = cursor.fetchall()

    completesL = [j for x in data for j in x]  # create list of completed key booleans
    completesDict = mapCompletesDict(completesL)


    return json.dumps(completesDict)

@app.route('/deleteUser', methods=['POST'])
def set_deleted_user():
    dUserID = (request.json["deletedUserID"])
    print(dUserID)
    updateKeyQuery = "UPDATE Login SET IsDeleted = 1 WHERE UserID={}".format(dUserID)
    cursor.execute(updateKeyQuery)
    conn.commit()
    return "ok"

@app.route('/exportUsers', methods=['GET'])
def export_users():
    exportQuery = ("SELECT * FROM Pieces")
    cursor.execute(exportQuery)
    data = cursor.fetchall()
    print(data)
    completesL = [j for x in data for j in x]
    temp = io.StringIO()
    writer = csv.writer(temp)
    for i in completesL:
            writer.writerow(i)

    mem = io.BytesIO()
    mem.write(temp.getvalue().encode('utf-8'))
    mem.seek(0)
    temp.close()

    return send_file(
        mem,
        as_attachment=True,
        attachment_filename='test.csv',
        mimetype='text/csv'
    )   


if __name__ == '__main__':
    app.run()