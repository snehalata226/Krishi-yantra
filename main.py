from flask import Flask, render_template,request
import os

from werkzeug.utils import secure_filename
import sqlite3
import smtplib
UPLOAD_FOLDER = 'static/upload'

app = Flask(__name__,template_folder='template')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
conn = sqlite3.connect("Krishi_yentra")
c = conn.cursor()


@app.route('/')
def home():
    return  render_template("home.html")

@app.route('/user_reg')
def home1a():
    return  render_template("User_register.html")

@app.route('/admin_log')
def admin_log():
    return render_template("Admin_login.html")

@app.route('/user_log')
def user_log():
    return render_template("login.html")

@app.route('/admin_add_product')
def admin_add_product():
    return render_template("Add_product.html")

@app.route('/add_rent_product')
def add_rent_product1():
    return render_template("Add_rent_product.html")


@app.route('/add_query/<a>')
def add_query(a):
    return render_template("Add_query.html",a=a)

@app.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        Name=request.form['uname']
        Sr_no=request.form['u_sr_no']
        Password=request.form['upassword']
        Address = request.form['uaddress']
        conn=sqlite3.connect("Krishi_yentra")
        conn.execute("INSERT INTO tbl_user_reg(Name,Sr_no,Password,Address) VALUES(?,?,?,?)",(Name,Sr_no,Password,Address))
        conn.commit()
        return  render_template("login.html")




@app.route('/add_product',methods=['POST'])
def add_product():
    if request.method == 'POST':
        f = request.files['ufile']
        e = f.filename
        filename = e
        filename = secure_filename(e)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Product_name = request.form['p_name']
        Product_price = request.form['p_price']
        Product_desc = request.form['p_desc']
        Product_availibilty = request.form['p_avail']
        conn = sqlite3.connect("Krishi_yentra")
        conn.execute("INSERT INTO tbl_product(Image_name,Product_name,Product_price,Product_desc,Product_availibilty) VALUES(?,?,?,?,?)",(e,Product_name,Product_price,Product_desc,Product_availibilty))
        conn.commit()
        return "Product Added Successfully"

@app.route('/add_enquiry',methods=['POST'])
def add_enquiry():
    if request.method == 'POST':
        User_Name = request.form['uname']
        Mobile = request.form['umobile']
        Query = request.form['uquery']
        Address = request.form['uaddress']
        conn = sqlite3.connect("Krishi_yentra")
        conn.execute("INSERT INTO tbl_add_query(User_Name,Mobile,Query,Address) VALUES(?,?,?,?)",(User_Name,Mobile,Query,Address))
        conn.commit()
        return "Product Added Successfully"


@app.route('/add_rent_product',methods=['POST'])
def add_rent_product():
    if request.method == 'POST':
        f = request.files['ufile']
        e = f.filename
        filename = e
        filename = secure_filename(e)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        P_name = request.form['p_name']
        Per_hour_price = request.form['p_price']
        P_desc = request.form['p_desc']
        Product_availibilty = request.form['p_avail']
        conn = sqlite3.connect("Krishi_yentra")
        conn.execute("INSERT INTO tbl_rent_products(P_image,P_name,Per_hour_price,P_desc,Product_availibilty) VALUES(?,?,?,?,?)",(e,P_name,Per_hour_price,P_desc,Product_availibilty))
        conn.commit()
        return "Rent Product Added Successfully"



@app.route('/admin_login',methods=['POST'])
def admin_login():
    if request.method == 'POST':
        Admin_email = request.form['email']
        Admin_password = request.form['password']
        conn = sqlite3.connect('Krishi_yentra')
        cur = conn.execute("SELECT * FROM tbl_admin WHERE Admin_email=? AND Admin_password=?",(Admin_email,Admin_password))
        rows1 = cur.fetchone()
        if rows1 == None:
            return  "Invalid Id & Password"
        else:
            return render_template('Add_product.html',)


@app.route('/user_login',methods=['POST'])
def login():
    if request.method == 'POST':
        Sr_no = request.form['usrno']
        Password = request.form['upassword']
        conn = sqlite3.connect('Krishi_yentra')
        cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Sr_no=? AND Password=?",(Sr_no,Password))
        rows1 = cur.fetchone()
        if rows1 == None:
            return  "Invalid Id & Password"
        else:
            cur = conn.execute("SELECT * FROM tbl_product")
            rows = cur.fetchall()
            return render_template('Product_details.html',rows1=rows1,rows=rows)



@app.route('/add/<a>/<b>')
def add(a,b):
    conn = sqlite3.connect("Krishi_yentra")
    cur = conn.execute("SELECT * FROM tbl_product WHERE Product_id=?",(a,))
    row = cur.fetchone()
    return render_template("Cart.html",row=row,b=b)

@app.route('/add_to_cart/<prod>/<cust>',methods=["POST"])
def add_to_cart(prod,cust):
    if request.method=='POST':
        qty = request.form['quantity']
        conn=sqlite3.connect("Krishi_yentra")
        cur = conn.execute("SELECT * FROM tbl_product WHERE Product_id=?",(prod,))
        row = cur.fetchone()
        cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?", (cust,))
        rows = cur.fetchone()
        conn.execute("INSERT INTO tbl_cart(c_name,p_name,qty,price,customer_address)VALUES(?,?,?,?,?)",(rows[1], row[2], qty, row[3], rows[4]))
        conn.commit()
        cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?",(cust,))
        rows1 = cur.fetchone()
        cur = conn.execute("SELECT * FROM tbl_product")
        rows = cur.fetchall()
        return render_template("Product_details.html",rows1=rows1,rows=rows)

@app.route('/checkout/<a>')
def  checkout(a):
    conn = sqlite3.connect("Krishi_yentra")
    cur = conn.execute("SELECT * FROM tbl_cart WHERE c_name=?",(a,))
    rows = cur.fetchall()
    if rows == None:
        return render_template("Bill.html", a=a, msg="U Seleced Nothing!")
    else:
        total = 0
        for row in rows:
            print(row)
            total = (int(row[3]) * int(row[4])) + total

        for row in rows:
            conn.execute(
                "INSERT INTO tbl_bill(C_name,Product_name,Product_qty,Product_price,Total_price,Address)VALUES(?,?,?,?,?,?)",
                (a, row[2], row[3], row[4], total, row[5]))
            conn.commit()
        conn.execute("DELETE FROM tbl_cart WHERE c_name=?", (a,))
        conn.commit()

        return render_template("Bill.html",rows=rows,total=total,a=a)

@app.route('/bill_histry/<a>')
def bill_histry(a):
    conn=sqlite3.connect("Krishi_yentra")
    cur = conn.execute("SELECT * FROM tbl_bill WHERE C_name=?",(a,))
    rows = cur.fetchall()
    print(rows)
    if rows == []:
        cust=[]
        return render_template("Bill_histry.html",a=a,msg="U Dont have any order histry!",cust=cust)
    else:
        cust = rows[0]
        return render_template("Bill_histry.html",rows=rows,cust=cust,a=a)

@app.route('/home/<a>')
def home1(a):
    conn = sqlite3.connect('Krishi_yentra')
    cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?", (a,))
    rows1 = cur.fetchone()
    cur = conn.execute("SELECT * FROM tbl_product")
    rows = cur.fetchall()
    return render_template('Product_details.html',rows1=rows1,rows=rows)

@app.route('/rent_product/<a>')
def rent(a):
    conn=sqlite3.connect("Krishi_yentra")
    cur=conn.execute("SELECT * FROM tbl_rent_products")
    rows=cur.fetchall()
    return render_template("Rent_product.html",rows=rows,a=a)



@app.route('/add_rent/<a>/<b>')
def add_rent(a,b):
    conn = sqlite3.connect("Krishi_yentra")
    cur = conn.execute("SELECT * FROM tbl_rent_products WHERE R_p_id=?",(a,))
    row = cur.fetchone()
    return render_template("Rent_add.html",row=row,b=b)

@app.route('/add_to_rent/<prod>/<cust>',methods=["POST"])
def add_to_rent(prod,cust):
    if request.method=='POST':
        rent_hours = request.form['uhours']
        conn=sqlite3.connect("Krishi_yentra")
        cur = conn.execute("SELECT * FROM tbl_rent_products WHERE R_p_id=?",(prod,))
        row = cur.fetchone()
        conn.execute("INSERT INTO tbl_rent_cart(c_name,p_name,p_h_price,rent_hours)VALUES(?,?,?,?)",(cust,row[2],row[3],rent_hours))
        conn.commit()
        cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?",(cust,))
        rows1 = cur.fetchone()
        cur = conn.execute("SELECT * FROM tbl_rent_products")
        rows = cur.fetchall()
        return render_template("Product_details.html",rows1=rows1,rows=rows)

@app.route('/rent_checkout/<a>')
def  rent_checkout(a):
    conn = sqlite3.connect("Krishi_yentra")
    cur = conn.execute("SELECT * FROM tbl_rent_cart WHERE c_name=?",(a,))
    rows = cur.fetchall()
    if rows == None:
        return render_template("Rent_bill.html",a=a,msg="U Seleced Nothing!")
    else:
        total = 0
        for row in rows:
            print(row)
            total = (int(row[3])*int(row[4]))+total

        for row in rows:
            conn.execute("INSERT INTO tbl_rent_bill(C_name,Product_name,Product_hours,Product_price,Total_price)VALUES(?,?,?,?,?)", (a,row[2],row[3],row[4],total))
            conn.commit()
        conn.execute("DELETE FROM tbl_rent_cart WHERE c_name=?",(a,))
        conn.commit()
        return render_template("Rent_bill.html",rows=rows,total=total,a=a)

@app.route('/rent_history/<a>')
def rent_history(a):
    conn=sqlite3.connect("Krishi_yentra")
    cur = conn.execute("SELECT * FROM tbl_rent_bill WHERE C_name=?",(a,))
    rows = cur.fetchall()
    print(rows)
    if rows == []:
        cust=[]
        return render_template("Rent_bill_histry.html",a=a,msg="U Dont have any order histry!",cust=cust)
    else:
        cust = rows[0]
        return render_template("Rent_bill_histry.html",rows=rows,cust=cust,a=a)

@app.route('/product_details/<a>')
def product_details(a):
    conn = sqlite3.connect('Krishi_yentra')
    cur = conn.execute("SELECT * FROM tbl_user_reg WHERE Name=?", (a,))
    rows1 = cur.fetchone()
    cur = conn.execute("SELECT * FROM tbl_product")
    rows = cur.fetchall()
    return render_template('Product_details.html',rows1=rows1,rows=rows)


@app.route('/purchase_list')
def purchase_list():
    conn = sqlite3.connect('Krishi_yentra')
    cur = conn.execute("SELECT * FROM tbl_bill")
    rows = cur.fetchall()
    return render_template('Purchase_details.html',rows=rows)

@app.route('/query_list')
def query_list():
    conn = sqlite3.connect('Krishi_yentra')
    cur = conn.execute("SELECT * FROM tbl_add_query")
    rows = cur.fetchall()
    return render_template('Query_details.html',rows=rows)

@app.route('/user_list')
def user_list():
    conn = sqlite3.connect('Krishi_yentra')
    cur = conn.execute("SELECT * FROM tbl_user_reg")
    rows = cur.fetchall()
    return render_template('User_details.html',rows=rows)


@app.route('/product_list')
def admin_product_list():
    conn = sqlite3.connect('Krishi_yentra')
    cur = conn.execute("SELECT * FROM tbl_product")
    rows = cur.fetchall()
    return render_template('Admin_product_details.html',rows=rows)


@app.route('/rent_list')
def rent_list():
    conn = sqlite3.connect('Krishi_yentra')
    cur = conn.execute("SELECT * FROM tbl_rent_bill")
    rows = cur.fetchall()
    return render_template('Rent_details.html',rows=rows)

@app.route('/logout')
def logout():
    return render_template("home.html")

if __name__=="__main__":
    app.run(host="0.0.0.0")