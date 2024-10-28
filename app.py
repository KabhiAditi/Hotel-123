from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def get_db_connection():
    conn = psycopg2.connect(
        dbname="Hotel",   
        user="postgres",              
        password="Aditi0307",        
        host="localhost"              
    )
    return conn

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/rooms')
def rooms():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM room WHERE is_available = TRUE")
    rooms = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('rooms.html', rooms=rooms)


@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM room WHERE room_id = %s", (room_id,))
    room = cur.fetchone()
    
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_contact = request.form['customer_contact']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        
        
        cur.execute("""
            INSERT INTO booking (customer_name, room_id, check_in, check_out)
            VALUES (%s, %s, %s, %s)
        """, (customer_name, room_id, check_in, check_out))
        
        
        cur.execute("""
            UPDATE room SET is_available = FALSE WHERE room_id = %s
        """, (room_id,))
        
        conn.commit()
        flash("Room booked successfully", "success")
        cur.close()
        conn.close()
        return redirect(url_for('rooms'))
    
    cur.close()
    conn.close()
    return render_template('booking.html', room=room)

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    
    
    cur.execute("""
        SELECT booking_id, customer_name, room_id, check_in, check_out
        FROM booking
        WHERE is_completed = FALSE
        ORDER BY check_in DESC
    """)
    bookings = cur.fetchall()
    
    cur.close()
    conn.close()
    return render_template('dashboard.html', bookings=bookings)

@app.route('/checkout/<int:booking_id>')
def checkout(booking_id):
    return render_template('rating.html', booking_id=booking_id)

@app.route('/submit_rating/<int:booking_id>', methods=['POST'])
def submit_rating(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    rating = request.form['rating']
    comments = request.form['comments']
    
    cur.execute("""
        INSERT INTO rating (booking_id, rating, comments)
        VALUES (%s, %s, %s)
    """, (booking_id, rating, comments))
    
    conn.commit()
    flash("Thank you for your feedback!", "success")
    cur.close()
    conn.close()
    
    return redirect(url_for('payment', booking_id=booking_id))


@app.route('/payment/<int:booking_id>')
def payment(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT due_amount FROM booking WHERE booking_id = %s", (booking_id,))
    due_amount = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    return render_template('payment.html', due_amount=due_amount, booking_id=booking_id)


@app.route('/confirm_payment/<int:booking_id>', methods=['POST'])
def confirm_payment(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    
    cur.execute("""
        UPDATE booking SET is_paid = TRUE, is_completed = TRUE WHERE booking_id = %s
    """, (booking_id,))
    
    
    cur.execute("""
        UPDATE room SET is_available = TRUE WHERE room_id = (
            SELECT room_id FROM booking WHERE booking_id = %s
        )
    """, (booking_id,))
    
    conn.commit()
    flash("Payment completed successfully!", "success")
    cur.close()
    conn.close()
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
