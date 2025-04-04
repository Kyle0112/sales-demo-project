from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
import os
from dotenv import load_dotenv
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

load_dotenv()
app = Flask(__name__)
CORS(app)

# Use RDS connection via environment variables (set in Elastic Beanstalk)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('RDS_USERNAME')}:{os.getenv('RDS_PASSWORD')}@"
    f"{os.getenv('RDS_HOSTNAME')}:{os.getenv('RDS_PORT')}/{os.getenv('RDS_DB_NAME')}"
) if os.getenv('RDS_HOSTNAME') else os.getenv('DATABASE_URL', 'sqlite:///sales.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
db = SQLAlchemy(app)



# Updated Sale model
class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)  # Changed to db.Date
    amount = db.Column(db.Float, nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            jwt.decode(token.split()[1], app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth.get('username') == 'user' and auth.get('password') == 'pass':
        token = jwt.encode(
            {'user': 'user', 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config['SECRET_KEY']
        )
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/sales', methods=['GET'])
@token_required
def get_sales():
    try:
        sales = Sale.query.all()
        return jsonify([{'id': s.id, 'date': s.date.isoformat(), 'amount': s.amount} for s in sales])
    except Exception as e:
        print(f"Error in get_sales: {e}")
        return jsonify({'message': 'Failed to retrieve sales'}), 500

@app.route('/sales', methods=['POST'])
@token_required
def create_sale():
    data = request.json
    if not data.get('date') or not data.get('amount'):
        return jsonify({'message': 'Missing date or amount'}), 400
    new_sale = Sale(date=data['date'], amount=float(data['amount']))
    db.session.add(new_sale)
    db.session.commit()
    return jsonify({'message': 'Sale created'}), 201

@app.route('/sales/<int:id>', methods=['PUT'])
@token_required
def update_sale(id):
    sale = Sale.query.get_or_404(id)
    data = request.json
    sale.date = data.get('date', sale.date)
    sale.amount = float(data.get('amount', sale.amount))
    db.session.commit()
    return jsonify({'message': 'Sale updated'})

@app.route('/sales/<int:id>', methods=['DELETE'])
@token_required
def delete_sale(id):
    sale = Sale.query.get_or_404(id)
    db.session.delete(sale)
    db.session.commit()
    return jsonify({'message': 'Sale deleted'})

@app.route('/predict', methods=['GET'])
@token_required
def predict_sale():
    sales = Sale.query.all()
    if len(sales) < 2:
        return jsonify({'message': 'Need at least 2 sales for prediction'}), 400
    df = pd.DataFrame([(i, s.amount) for i, s in enumerate(sales)], columns=['week', 'amount'])
    X = df['week'].values.reshape(-1, 1)
    y = df['amount'].values
    model = LinearRegression().fit(X, y)
    next_week = np.array([[len(sales)]])
    prediction = model.predict(next_week)[0]
    plt.figure(figsize=(6, 4))
    plt.plot(df['week'], df['amount'], label='Past Sales', marker='o')
    plt.plot([len(sales)], prediction, label='Predicted', marker='x', color='red')
    plt.xlabel('Week')
    plt.ylabel('Sales')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
    buf.close()
    plt.close()
    return jsonify({'predicted_next_sale': prediction, 'plot_url': plot_url})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)