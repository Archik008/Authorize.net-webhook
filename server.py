from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from payment import charge_credit_card


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class CarPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vin_code = db.Column(db.String(17), nullable=False)
    session_id = db.Column(db.String, nullable=False)  # Payment status
    is_paid = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Car {self.vin_code} - Paid: {self.is_paid}>'
        
# Checking car's vin code and loading payment form. Session id is using to save payment status
@app.route('/paycarfax/<vin_code>/<session_id>', methods=["GET"])
def payment_form(vin_code, session_id):

    carReport = CarPayment.query.filter_by(vin_code=vin_code, session_id=session_id).first()

    if carReport:
        is_paid = carReport.is_paid
        if is_paid:
            return render_template('success.html')
        else:
            return render_template('fail.html')
    
    if len(vin_code) != 17:
        abort(400, description="Wrong car VIN code")

    return render_template('payment_form.html')

# Proceeding payment for carfax report
@app.route('/payment', methods=['POST'])
def process_payment():
    data = request.get_json()

    vin_code = data.get('vin_code')
    session_id = data.get('session_id')
    card_number = data.get('card_number')
    exp_date = data.get('exp_date')
    card_code = data.get('card_code')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    zip_code = data.get('zip_code')
    email = data.get('email')

    credit_card_succed = charge_credit_card(vin_code, card_number, exp_date, card_code, first_name, last_name, address, city, state, zip_code, email)
    
    car_report = CarPayment(vin_code=vin_code, session_id=session_id)

    if credit_card_succed:
        car_report.is_paid = True
    else:
        car_report.is_paid = False

    db.session.add(car_report)
    db.session.commit()

    if car_report.is_paid:
        return jsonify({"is_paid": True}), 200
    else:
        abort(400, description="Payment failed!")

            
@app.route('/checkpayment/<vin_code>/<session_id>', methods=["POST"])
def checking_payment(vin_code, session_id):
    car = CarPayment.query.filter_by(vin_code=vin_code, session_id=session_id).first()
    if car:
        return jsonify({"is_paid": True}), 200
    else:
        return jsonify(error="Not found"), 400
    
@app.route('/fail')
def render_fail():
    return render_template('fail.html')

@app.route('/success')
def render_success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')