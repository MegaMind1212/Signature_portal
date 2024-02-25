from flask import Flask, render_template, request, send_file, jsonify
from flask_mail import Mail, Message
import base64

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.example.com'  # Replace with your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@example.com'  # Replace with your email address
app.config['MAIL_PASSWORD'] = 'your_password'  # Replace with your email password

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_signature', methods=['POST'])
def save_signature():
    signature_data = request.form['signature']
    signature_type = request.form['signature_type']

    # Decode base64 signature data
    signature_data = base64.b64decode(signature_data.split(',')[1])

    # Save the signature to a file
    filename = 'signature.' + signature_type
    with open(filename, 'wb') as f:
        f.write(signature_data)

    # Return the filename to download
    return send_file(filename, as_attachment=True)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    email = data['email']
    signature_data = data['signature']

    # Create a message object
    msg = Message('Signature Attached', sender='your_email@example.com', recipients=[email])
    msg.body = 'Please find the signature attached.'
    msg.attach('signature.jpg', 'image/jpeg', base64.b64decode(signature_data.split(',')[1]))

    # Send the email
    try:
        mail.send(msg)
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
