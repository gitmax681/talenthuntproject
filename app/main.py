from flask import Flask, redirect, url_for, render_template, request, session, flash,  send_from_directory
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
from datetime import datetime
import os
import qrcode
from svglib.svglib import svg2rlg




def qrgen(text):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img


app = Flask(__name__)
app.config['SECRET_KEY'] = 'randomsecretkey'
app.config['UPLOAD_FOLDER'] = './pdfs'
data = {}



def pdfgen(
    name, 
    dob, 
    gender, 
    addhr,
    email,
    phno,
    clas,
    schlname,
    schladdr,
    schlcity,
    schldist, 
    schlstate,
    schlpin,
    board,
    hname,
    haddr,
    hcity,
    hdist, 
    hstate,
    hpin
    ):
    FILENAME = f"{name}-{str(datetime.now())}.pdf"
    path = os.path.join('./pdfs/',  FILENAME)
    c = canvas.Canvas(path, pagesize=A4)
    c.setAuthor("2022-2023 St Jude XII")
    c.setTitle("Registration")
    c.setSubject("Registration Confirmation pdf")

    # borders of pdf
    c.line(20, 20, 20, 820)  # left line
    c.line(20, 820, 575, 820)  # top line
    c.line(575, 820, 575, 20)  # right line
    c.line(575, 20, 20, 20)  # bottom line

    # invoice top section division
    c.line(20, 700, 575, 700)
    c.line(450, 820, 450, 700)
    # static writings
    c.setFont("Helvetica-Bold", 28)
    c.drawString(130, 760, "Talent Hunt 2022-2023")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 730, "Student Registration Details")
    # insertion of qr code and logo
    image = svg2rlg('talenthunt.svg')
    c.drawInlineImage(qrgen("sorry, functions isn't setup yet"),
                      460, 710, height=100, width=100)
    renderPDF.draw(image, c, 0, 685)

    # static writings for details
    c.setFont("Helvetica", 16)
    c.drawString(40, 650, "Name ")
    c.drawString(40, 620, "Date Of Birth ")
    c.drawString(40, 590, "Gender ")
    c.drawString(40, 560, "Addhhar No ")
    c.drawString(40, 530, "Email Address ")
    c.drawString(40, 500, "Mobile Number ")
    c.drawString(40, 470, "Class ")
    
    c.drawString(40,  440, "School")
    c.drawString(40,  350, "Board Of Education")
    c.drawString(40,  310, "Residence")
    # dynamic writings for details
    c.drawString(200, 650, f":  {name}")    
    c.drawString(200, 620, f":  {dob}") 
    c.drawString(200, 590, f":  {gender}") 
    c.drawString(200, 560, f":  {addhr}") 
    c.drawString(200, 530, f":  {email}") 
    c.drawString(200, 500, f":  {phno}") 
    c.drawString(200, 470, f":  {clas}") 
    c.drawString(200, 440, f":  {schlname}")
    c.drawString(200, 410, f"   {schladdr}")
    c.drawString(200, 380, f"   {schlcity}, {schldist}, {schlstate}, {schlpin}")
    c.drawString(200, 350, f":  {board}")
    c.drawString(200, 310, f':  {hname}')
    c.drawString(200, 280, f'   {haddr}')
    c.drawString(200, 250, f'   {hcity},{hdist}, {hstate}, {hpin}')
    c.line(20, 220, 575, 220)

    # footer
    c.setFont("Helvetica", 14)
    c.drawString(40,  200, "1. Students are requested to take a copy of this pdf and keep it with them")
    c.drawString(40,  180, "   until the admit card is issued.")
    c.drawString(40, 160, "2. Students are requested to reach the exam center 1 hour prior to the exam.")
    c.drawString(40,  140, "3. Admit cards will be issued  1 month prior to the exam.")
    c.drawString(40,  120, "4. Use of Electic Devices like Mobiles, Smart Watches, Calculators are strictly")
    c.drawString(40,  100, "   Prohibited.")
    c.drawString(40,  80, "5. Attempt of Malpractices will lead to disqualification of the Candidate.")
    c.drawString(40,  60, "5. The Details of this pdf will be final and any error in the students biodata")
    c.drawString(40,  40, "   will lead to disqualification of the Candidate.")
    c.setFont("Helvetica", 10)
    c.drawString(360, 40, f"Issued On: {datetime.now()}")

    c.showPage()
    c.save()
    return FILENAME


@app.route('/signin/', methods=['POST'])
def signin():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['email']
        if len(mail) != 0 and len(name) != 0:
            print('success')
            data['name'] = name
            data['mail'] = mail
            return redirect(url_for('register',email= mail, usrname=name))
        else:
            return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=('GET', 'POST'))
def home():
    return render_template('index.html')


@app.route('/finalregister', methods=['POST'])
def finalregister():
    if request.method == 'POST':
        d = request.form
        filename = pdfgen(d['fname']+' ' + d['lname'], d['dob'], d['gender'], d['adhr'], d['email']
        , d['phno'], d['class'],  d['schlname'], d['schladdr'], d['schlcity'],d['schldist'],
         d['schlstate'], d['schlpin'], d['medium'], d['hname'], d['haddr'], d['hcity'], 
         d['hdist'], d['hstate'], d['hpin'])
        print(filename)
        return redirect(url_for('success', filename=filename))
    else:
        return redirect(url_for('home'))


@app.route('/register?email=<email>&usrname=<usrname>', methods=['GET', 'POST'])
def register(usrname, email):
    return render_template('register.html', usrname=usrname, email=email)


@app.route('/registerstatus?filename=<filename>')
def success(filename):
    return send_from_directory(directory='./pdfs/', path=filename)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
