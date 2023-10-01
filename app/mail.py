import smtplib
from email.mime.text import MIMEText
from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app
)
from app.db import get_db




bp = Blueprint('mail', __name__, url_prefix="/")


@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    print(search)
    db, c = get_db()

    if search is None:
        c.execute("SELECT * FROM email")
    else:
        c.execute("SELECT * from email WHERE content like %s", (f'%{search}%',))
    mails = c.fetchall()
    return render_template('mails/index.html', mails=mails)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('Email is obligatory!')
        if not subject:
            errors.append('Subject is obligatory!')
        if not content:
            errors.append('Content is obligatory!')

        if len(errors) == 0:
            send(to=email, subject=subject, content=content)
            db, c = get_db()
            c.execute("INSERT INTO email (email, subject, content) VALUES (%s, %s, %s)", (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))
        
        else:
            for error in errors:
                flash(error)
               
    return render_template('mails/create.html')


def send(to, subject, content):
    account = current_app.config['MY_ADDRESS']
    password = current_app.config['PASSWORD']
    
    html_template = f"""\
            <html>
                <body>
                 <p>This is a test with <strong>HTML include!<strong/></p>

                 <p>{content}</p>

               <i>Made in Python with ♥<i/>
    </body>
</html>
    
            """
    
    message = MIMEText(html_template, "html")
    message["Subject"] = subject
    message["To"] = to

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as server:
        server.starttls()
        server.login(account, password)

        server.sendmail(from_addr=account,
                         to_addrs=to,
                           msg=message.as_string())



