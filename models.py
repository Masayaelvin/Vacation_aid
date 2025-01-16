from backend import db
from datetime import datetime

# Define Models
class User(db.Model):
    """User model representing hosts and customers."""
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(200), default='default.jpg')
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Enum('host', 'customer', name='user_roles'), default='customer', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relationships
    properties = db.relationship('Property', backref='host', lazy=True)
    bookings = db.relationship('Booking', backref='customer', lazy=True)

    def __repr__(self):
        return f'<User {self.user_id}: {self.email}>'


class Property(db.Model):
    """Property model for host listings."""
    __tablename__ = 'properties'
    property_id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    excursions = db.relationship('Excursion', backref='property', lazy=True)
    bookings = db.relationship('Booking', backref='property', lazy=True)


class Excursion(db.Model):
    """Excursion model for activities offered at a property."""
    __tablename__ = 'excursions'
    excursion_id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)


class Booking(db.Model):
    """Booking model for reservations."""
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    booking_excursions = db.relationship('BookingExcursion', backref='booking', lazy=True)
    rides = db.relationship('Ride', backref='booking', lazy=True)
    flights = db.relationship('Flight', uselist=False, backref='booking')
    payment = db.relationship('Payment', uselist=False, backref='booking')


class BookingExcursion(db.Model):
    """Association table for bookings and excursions."""
    __tablename__ = 'booking_excursions'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    excursion_id = db.Column(db.Integer, db.ForeignKey('excursions.excursion_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)


class Ride(db.Model):
    """Ride model for transportation associated with a booking."""
    __tablename__ = 'rides'
    ride_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    pickup_location = db.Column(db.String(200), nullable=False)
    dropoff_location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)


class Flight(db.Model):
    """Flight model for flight reservations."""
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    airline = db.Column(db.String(100), nullable=False)
    flight_number = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)


class Payment(db.Model):
    """Payment model for transactions."""
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'completed', 'failed', name='payment_status'), default='pending', nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)


# Initialize the database
db.create_all()
