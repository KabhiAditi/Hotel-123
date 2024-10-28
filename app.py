from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure secret key in production!

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="Hotel",   # Change as per your database
        user="postgres",              # Replace with your database username
        password="Aditi0307",        # Replace with your database password
        host="localhost"              # Change if your database is hosted elsewhere
    )
    return conn

# Home route - uses base.html template
@app.route('/')
def home():
    return render_template('base.html')

# Rooms available page
@app.route('/rooms')
def rooms():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM room WHERE is_available = TRUE")
    rooms = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('rooms.html', rooms=rooms)

# Booking a room page
@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch room details
    cur.execute("SELECT * FROM room WHERE room_id = %s", (room_id,))
    room = cur.fetchone()
    
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_contact = request.form['customer_contact']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        
        # Insert new booking into the booking table
        cur.execute("""
            INSERT INTO booking (customer_name, room_id, check_in, check_out)
            VALUES (%s, %s, %s, %s)
        """, (customer_name, room_id, check_in, check_out))
        
        # Mark room as unavailable
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

# Dashboard page for hotel staff (shows all bookings)
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch all bookings that are not completed for display on the dashboard
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

# Submit rating for a booking after checkout
@app.route('/submit_rating/<int:booking_id>', methods=['POST'])
def submit_rating(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    rating = request.form['rating']
    comments = request.form['comments']
    
    # Insert rating into the rating table
    cur.execute("""
        INSERT INTO rating (booking_id, rating, comments)
        VALUES (%s, %s, %s)
    """, (booking_id, rating, comments))
    
    conn.commit()
    flash("Thank you for your feedback!", "success")
    cur.close()
    conn.close()
    
    return redirect(url_for('payment', booking_id=booking_id))

# Payment route after rating submission
@app.route('/payment/<int:booking_id>')
def payment(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Retrieve the due amount for the booking
    cur.execute("SELECT due_amount FROM booking WHERE booking_id = %s", (booking_id,))
    due_amount = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    return render_template('payment.html', due_amount=due_amount, booking_id=booking_id)

# Confirm payment route to complete the payment process
@app.route('/confirm_payment/<int:booking_id>', methods=['POST'])
def confirm_payment(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Mark booking as paid
    cur.execute("""
        UPDATE booking SET is_paid = TRUE, is_completed = TRUE WHERE booking_id = %s
    """, (booking_id,))
    
    # Mark room as available again
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
