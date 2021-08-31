from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
app = Flask(__name__,static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/')
def home():
   return render_template('farmhome.html')

@app.route('/get/')
def get():
   return render_template('learnc3.html')

@app.route('/get2/')
def get2():
   data = [
      ("01-01-2020", 1597),
      ("02-01-2020", 1456),
      ("03-01-2020", 1908),
      ("04-01-2020", 896),
      ("05-01-2020", 755),
      ("06-01-2020", 453),
      ("07-01-2020", 1100),
      ("08-01-2020", 1235),
      ("09-01-2020", 1478),
      ("10-01-2020", 1740.2),
      ("11-01-2020", 24.2),
   ]

   labels = [row [0] for row in data]
   values = [row [1] for row in data]
   
   return render_template('graph.html', labels=labels, values=values)

@app.route('/smple/')
def smple():
   return render_template('trypagin.html')

@app.route('/beta/')
def beta():
   return render_template('betadev.html')

@app.route('/smple2/')
def smple2():
   con = sql.connect("bmppub.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("Select * from storage")

   rows = cur.fetchall();
   return render_template('trypagin2.html',rows = rows)

@app.route('/addusnmpassw/')
def new_farmer():
   return render_template('usnm.html')

@app.route('/login/')
def login():
   return render_template("userlogin.html")

@app.route('/userhome/')
def userhome():
   return render_template("userhome.html")

@app.route('/addnew/',methods = ['POST', 'GET'])
def addnew():
   
   if request.method == 'POST':
      try:
         usnm = request.form['usnm']
         passw = request.form['passw']
         passw1 = request.form['passw1']
         
         if passw == passw1:
            with sql.connect("userlog.db") as con:
               cur = con.cursor()
               
               cur.execute("INSERT INTO data (Username,Password) VALUES (?,?)",(usnm,passw) )
               
               con.commit()
               msg = "Successfully Registered"
         
         else:
            msg = "Passwords Did Not Match"
            return render_template("result.html",msg = msg)
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/page/',methods = ['POST', 'GET'])
def page():
   if request.method == 'POST':

      usnm = request.form['usnm']
      passw = request.form['passw']
      
      conn = sql.connect("userlog.db")
      cr = conn.cursor()

      cr.execute("SELECT * FROM data WHERE Username= ? and Password= ?",(usnm, passw))
      passcheck = cr.fetchone()
      if passcheck:
         return redirect("/userhome/")
      else :
         return render_template("wrong.html")


@app.route('/subs/')
def subs():
   con = sql.connect("bmppub.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("Select * from storage ORDER BY Time DESC ")

   rows = cur.fetchall();
   return render_template("listpub.html",rows = rows)

@app.route('/subsearch/')
def search():
   con = sql.connect("bmppub.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("Select * from storage")

   rows = cur.fetchall();
   return render_template("searchlistpub.html",rows = rows)
      

if __name__ == '__main__':
    app.run(debug=False,host='192.168.1.87')
    #app.run(debug=False)
