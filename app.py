from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import qrcode
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/qrcodes'

# Ensure directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if request.method == 'POST':
        url = request.form.get('url')
        
        if not url:
            return redirect('/')
        
        # Generate a unique filename to avoid cache issues
        timestamp = int(time.time())
        filename = f"qrcode_{timestamp}.png"
        
        # Create QR code
        qr = qrcode.make(url)
        
        # Save the QR code
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        qr.save(filepath)
        
        # Return to the index page with the image path
        image_url = url_for('static', filename=f'qrcodes/{filename}')
        return redirect(url_for('index', image=image_url))

@app.route('/static/qrcodes/<filename>')
def serve_qrcode(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)