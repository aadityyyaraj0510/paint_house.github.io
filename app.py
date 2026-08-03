import os
import urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'painthouse_super_secret_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    upi_id = db.Column(db.String(100), default="paint.house@upi")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ColorItem(db.Model):
    __tablename__ = 'color_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hex_code = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(20), default='WHEEL')
    price_per_room = db.Column(db.Float, default=499.00)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    id_proof = db.Column(db.String(50), nullable=True)
    color = db.Column(db.String(50), nullable=False)
    design_style = db.Column(db.String(50), nullable=False)
    booking_date = db.Column(db.String(20), nullable=False)
    booking_time = db.Column(db.String(20), nullable=False)
    rooms = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    amount = db.Column(db.Float, default=499.00)
    payment_mode = db.Column(db.String(20), default='COD')
    payment_status = db.Column(db.String(20), default='PENDING')
    payment_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def seed_colors():
    if ColorItem.query.count() == 0:
        # 100+ Professional Unique Colors
        wheel_data = [
            ("Crimson Red", "#E53935"), ("Ruby Flame", "#D32F2F"), ("Cherry Pop", "#C62828"), ("Sunset Rose", "#B71C1C"),
            ("Bright Orange", "#F57C00"), ("Tangerine Dream", "#EF6C00"), ("Amber Glow", "#E65100"), ("Autumn Leaf", "#D84315"),
            ("Lemon Zest", "#FBC02D"), ("Sunny Yellow", "#F9A825"), ("Golden Ray", "#F57F17"), ("Mellow Yellow", "#FFEE58"),
            ("Lime Green", "#7CB342"), ("Spring Leaf", "#689F38"), ("Forest Tint", "#558B2F"), ("Olive Minimal", "#33691E"),
            ("Emerald Mint", "#00897B"), ("Teal Breeze", "#00796B"), ("Deep Teal", "#004D40"), ("Aqua Marine", "#00ACC1"),
            ("Sky Blue", "#039BE5"), ("Ocean Wave", "#0288D1"), ("Royal Azure", "#0277BD"), ("Navy Deep", "#01579B"),
            ("Indigo Night", "#3F51B5"), ("Royal Indigo", "#303F9F"), ("Deep Purple", "#512DA8"), ("Vivid Violet", "#4527A0"),
            ("Magenta Glow", "#C2185B"), ("Pink Blossom", "#AD1457"), ("Rose Blush", "#880E4F"), ("Soft Peach", "#FF8A65"),
            ("Warm Sand", "#D7CCC8"), ("Muted Earth", "#BCAAA4"), ("Taupe Gray", "#A1887F"), ("Coffee Bean", "#8D6E63"),
            ("Slate Minimal", "#78909C"), ("Steel Blue", "#607D8B"), ("Graphite Dark", "#455A64"), ("Charcoal Tone", "#37474F"),
            ("Pure Silver", "#B0BEC5"), ("Cloud White", "#ECEFF1"), ("Pearl Ivory", "#FAFAFA"), ("Vanilla Cream", "#FFFDE7"),
            ("Mint Cream", "#E8F5E9"), ("Ice Blue", "#E3F2FD"), ("Lavender Mist", "#EDE7F6"), ("Rose Tint", "#FCE4EC"),
            ("Sunny Cream", "#FFFDE7"), ("Peach Tint", "#FBE9E7"), ("Coral Blaze", "#FF3B30"), ("Neon Lime", "#AEEA00"),
            ("Electric Cyan", "#00E5FF"), ("Deep Fuchsia", "#F50057"), ("Neon Amber", "#FFAB00"), ("Chartreuse", "#76FF03"),
            ("Turquoise Glow", "#1DE9B6"), ("Deep Amethyst", "#651FFF"), ("Sunset Coral", "#FF6E40"), ("Pastel Mint", "#B9F6CA"),
            ("Ice Cyan", "#80D8FF"), ("Soft Lilac", "#EA80FC"), ("Warm Ochre", "#FFD54F"), ("Muted Teal", "#4DB6AC"),
            ("Dusty Rose", "#F06292"), ("Slate Gray Dark", "#37474F"), ("Classic Beige", "#D7CCC8"), ("Burnt Sienna", "#BF360C"),
            ("Teal Deep", "#00695C"), ("Indigo Muted", "#5C6BC0"), ("Forest Emerald", "#2E7D32"), ("Golden Yellow", "#F57F17"),
            ("Crimson Dark", "#B71C1C"), ("Blue Steel", "#455A64"), ("Violet Dusk", "#7B1FA2"), ("Teal Bright", "#00B0FF"),
            ("Orange Peel", "#FF6D00"), ("Lime Punch", "#AEEA00"), ("Pink Bubblegum", "#FF4081"), ("Cyan Breeze", "#00B8D4"),
            ("Purple Storm", "#7C4DFF"), ("Amber Warm", "#FF6F00"), ("Green Mint", "#00E676"), ("Blue Deep", "#0D47A1"),
            ("Red Velvet", "#880E4F"), ("Yellow Pastel", "#FFF59D"), ("Gray Cool", "#CFD8DC"), ("Brown Mocha", "#4E342E"),
            ("Teal Aqua", "#00B4D8"), ("Rose Pink", "#FF80AB"), ("Indigo Slate", "#37474F"), ("Orange Sunset", "#FF7043"),
            ("Green Olive", "#558B2F"), ("Blue Sky", "#29B6F6"), ("Purple Royal", "#4A148C"), ("Yellow Bright", "#FFEA00"),
            ("Red Coral", "#FF5252"), ("Cyan Deep", "#006064"), ("Platinum Gray", "#90A4AE"), ("Champagne Gold", "#D4AF37")
        ]
        
        for name, hex_code in wheel_data:
            db.session.add(ColorItem(name=name, hex_code=hex_code, category='WHEEL', price_per_room=499.00))

        mixer_data = [
            ("Mixer Red", "#FF5252"), ("Mixer Blue", "#448AFF"), ("Mixer Green", "#69F0AE"),
            ("Mixer Yellow", "#FFEB3B"), ("Mixer Purple", "#E040FB"), ("Mixer Cyan", "#18FFFF")
        ]
        for name, hex_code in mixer_data:
            db.session.add(ColorItem(name=name, hex_code=hex_code, category='MIXER', price_per_room=499.00))

        db.session.commit()

with app.app_context():
    db.create_all()
    seed_colors()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/colors', methods=['GET'])
def get_colors():
    wheel_colors = ColorItem.query.filter_by(category='WHEEL').all()
    mixer_colors = ColorItem.query.filter_by(category='MIXER').all()
    return jsonify({
        "wheel_colors": [{"id": c.id, "name": c.name, "hex": c.hex_code, "price": c.price_per_room} for c in wheel_colors],
        "mixer_colors": [{"id": c.id, "name": c.name, "hex": c.hex_code, "price": c.price_per_room} for c in mixer_colors]
    })

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    res = [{"id": r.id, "name": r.customer_name, "rating": r.rating, "comment": r.comment, "date": r.created_at.strftime("%Y-%m-%d")} for r in reviews]
    return jsonify({"reviews": res})

@app.route('/api/reviews/add', methods=['POST'])
def add_review():
    if 'user_id' not in session:
        return jsonify({"error": "Please login to submit a review"}), 401
    data = request.get_json(silent=True) or {}
    rating = int(data.get('rating', 5))
    comment = data.get('comment', '').strip()
    if not comment:
        return jsonify({"error": "Comment cannot be empty"}), 400
    user = User.query.get(session['user_id'])
    rev = Review(user_id=user.id, customer_name=user.name, rating=rating, comment=comment)
    db.session.add(rev)
    db.session.commit()
    return jsonify({"message": "Review submitted successfully!"})

@app.route('/api/admin/update-color-price', methods=['POST'])
def update_color_price():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json(silent=True) or {}
    color = ColorItem.query.get(data.get('color_id'))
    if not color:
        return jsonify({"error": "Color not found"}), 404
    color.price_per_room = float(data.get('price'))
    db.session.commit()
    return jsonify({"message": f"Price updated successfully"})

@app.route('/api/admin/set-upi', methods=['POST'])
def set_admin_upi():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json(silent=True) or {}
    admin = User.query.get(session['user_id'])
    admin.upi_id = data.get('upi_id', '').strip()
    db.session.commit()
    return jsonify({"message": "Admin UPI updated"})

@app.route('/api/user/update-profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json(silent=True) or {}
    user = User.query.get(session['user_id'])
    user.name = data.get('name', '').strip()
    db.session.commit()
    return jsonify({"message": "Profile updated", "name": user.name})

@app.route('/api/get-upi-link', methods=['POST'])
def get_upi_link():
    data = request.get_json(silent=True) or {}
    amount = data.get('amount', 499)
    admin = User.query.filter_by(is_admin=True).first()
    payee_vpa = admin.upi_id if (admin and admin.upi_id) else "paint.house@upi"
    return jsonify({"upi_url": f"upi://pay?pa={payee_vpa}&pn=PaintHouse&am={amount}&cu=INR", "vpa": payee_vpa, "amount": amount})

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json(silent=True) or {}
        name, raw_email, password = data.get('name', '').strip(), data.get('email', '').strip(), data.get('password')
        is_admin = '/admin' in raw_email.lower()
        clean_email = raw_email.lower().replace('/admin', '').strip()
        if User.query.filter_by(email=clean_email).first():
            return jsonify({"error": "Email already registered"}), 400
        user = User(name=name, email=clean_email, password_hash=bcrypt.generate_password_hash(password).decode('utf-8'), is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        return jsonify({"message": "Success", "user": {"id": user.id, "name": user.name, "email": user.email, "is_admin": user.is_admin, "upi_id": user.upi_id}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True) or {}
        raw_email, password = data.get('email', '').strip(), data.get('password')
        clean_email = raw_email.lower().replace('/admin', '').strip()
        user = User.query.filter_by(email=clean_email).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid email or password"}), 401
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        return jsonify({"message": "Success", "user": {"id": user.id, "name": user.name, "email": user.email, "is_admin": user.is_admin, "upi_id": user.upi_id}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

@app.route('/api/delete-account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(session['user_id'])
    Booking.query.filter_by(user_id=user.id).delete()
    Review.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    session.clear()
    return jsonify({"message": "Account deleted"})

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    data = request.get_json(silent=True) or {}
    pay_mode = data.get('payment_mode', 'COD')
    booking = Booking(
        user_id=session['user_id'], full_name=data.get('full_name'), email=data.get('email'),
        phone=data.get('phone'), id_proof=data.get('id_proof', 'Not Provided'), color=data.get('color'),
        design_style=data.get('design_style'), booking_date=data.get('booking_date'), booking_time=data.get('booking_time'),
        rooms=int(data.get('rooms', 1)), notes=data.get('notes'), amount=float(data.get('amount', 499.00)),
        payment_mode=pay_mode, payment_status='PAID (UPI)' if pay_mode == 'ONLINE_UPI' else 'PENDING (COD)'
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"message": "Booking confirmed"})

@app.route('/api/admin/bookings', methods=['GET'])
def get_admin_bookings():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({"error": "Admin access denied"}), 403
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return jsonify({"bookings": [{
        "id": b.id, "full_name": b.full_name, "phone": b.phone, "color": b.color,
        "design_style": b.design_style, "booking_date": b.booking_date, "booking_time": b.booking_time,
        "rooms": b.rooms, "amount": b.amount, "payment_mode": b.payment_mode, "payment_status": b.payment_status
    } for b in bookings]})

@app.route('/api/user/history', methods=['GET'])
def get_user_history():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    bookings = Booking.query.filter_by(user_id=session['user_id']).order_by(Booking.created_at.desc()).all()
    return jsonify({"history": [{"id": b.id, "color": b.color, "date": b.booking_date, "amount": b.amount, "status": b.payment_status, "mode": b.payment_mode} for b in bookings]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)