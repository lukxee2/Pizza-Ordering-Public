from datetime import datetime
from flask import Flask, jsonify, json, render_template, request, session
import smtplib # IF IT ERRORS OUT THEN PLEASE INSTALL THIS!
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from waitress import serve

app = Flask(__name__)
orders={}

# Web Service Code (Request-Response)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chef')
def chef():
    return render_template('chef.html', orders=orders)

@app.route('/api/submitOrder', methods = ['POST', 'GET'])
def Submit():
    orderName=request.get_json()['name']
    orderContent=request.get_json()['contents']
    orderTime=datetime.now().strftime("%H:%M")
    orderTotal=request.get_json()['total']
    
    orders[orderName]={'name':orderName, 'contents':orderContent, 'total': orderTotal, 'time': orderTime, 'status': 'Not Started'}
    print(orders)

    return jsonify({"success": True})

@app.route('/api/sendEmail', methods = ['POST', 'GET'])
def Email():
    orderName=request.get_json()['name']
    orderContent=request.get_json()['contents']
    orderTime=datetime.now().strftime("%H:%M, %d/%m/%Y")
    orderTotal=request.get_json()['total']
    orderemail=request.get_json()['email']
    
    contentstr = joined_string = ", ".join(orderContent)
    
    smtp_server = '' # Email server here
    sender = '' # Email sender here
    user = '' # Email username here
    recipient = orderemail
    password = '' # Email password here
    server = smtplib.SMTP(host = smtp_server,port= 587)
    server.starttls()
    server.login(user = user, password = password)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Order Confirmation"
    msg['From'] = sender
    msg['To'] = recipient
    str = "<!DOCTYPE html><html> <body> <img class='d-block mx-auto mb-4' src='https://cdn.discordapp.com/attachments/659031245996556325/937846056497066044/KIM_Logo.webp' alt="" width='72' height='65'><br><h1 style='color:rgb(106, 45, 145);'>Thanks for Ordering with KimPizza!</h1> <p><br>Order name: {}<br>Time of Order: {}<br>Pizzas Ordered: {}<br>Total: £{}<br><br><a href='http://localhost:5000/viewOrder/{}'>Follow your order here!</a></p></body></html>".format(orderName, orderTime, contentstr, orderTotal, orderName)
    htmltext = MIMEText(str, 'html')
    msg.attach(htmltext)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()
    print(orderName, orderContent, orderTime, orderTotal, orderemail)
    return jsonify({"success": True})

@app.route('/api/UpdateOrder', methods = ['POST', 'GET'])
def Update():
    orderName=request.get_json()['name']
    orderStatus=request.get_json()['status']

    orders[orderName]['status'] = orderStatus
    print(orders[orderName])
    return jsonify({"success": True})

@app.route('/viewOrder/<name>')
def OrderProgress(name):
    return render_template("orderprogress.html", orders=orders, name=name)

if __name__ == "__main__":
    #app.debug = True
    #app.run(host="0.0.0.0")
    serve(app, host='0.0.0.0', port=5000)