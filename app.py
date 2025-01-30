from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.models import db, User, Car, Office
from helpers.auth_handler import hash_password, check_password, is_authenticated, get_current_user
from helpers.validators import validate_user_registration
from helpers.google_maps import get_office_locations
from config import Config
from datetime import datetime

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
LANGUAGES = {
    "en": {
        "welcome": "Welcome to Car Rental",
        "pickup_office": "Pickup Office",
        "pickup_date": "Pickup Date",
        "pickup_time": "Pickup Time",
        "return_office": "Return Office",
        "return_date": "Return Date",
        "return_time": "Return Time",
        "rent_for_days": "Rent According To Specific Criteria",
        "logout": "Logout",
        "login": "Login",
        "register": "Register",
        "office_map": "Office Map",
        "no_cars_found": "No cars found matching your criteria.",
        "results": "Results",
        "show_cars": "Show Cars",
        "back_to_home": "Back to Home",
        "sort_by": "Sort By",
        "transmission": "Transmission",
        "cost": "Cost",
        "deposit": "Deposit",
        "mileage": "Mileage",
        "age": "Age",
        "rental_cost": "Rental Cost",
        "filter_transmission": "Filter by Transmission",
        "all": "All",
        "automatic": "Automatic",
        "manual": "Manual",
        "sort_order": "Sort Order",
        "ascending": "Ascending",
        "descending": "Descending",
        "email": "Email",
        "password": "Password",
        "username": "Username",
        "country": "Country",
        "city": "City",
        "profile_picture": "Profile Picture",
        "profile_picture_optional": "Profile Picture (Optional)",
        "search": "Search",
        "select_pickup_office": "Select Pickup Office",
        "select_return_office": "Select Return Office",
        "search_results": "Search Results",
        "car_details": "Car Details",
        "office_information": "Office Information",
        "phone": "Phone",
        "home": "Home",
        "select_language": "Select Language",
        "register_now": "Register Now",
        "login_now": "Login Now",
        "confirm_password": "Confirm Password",
    },
    "tr": {
        "welcome": "Araba Kiralama'ya Hoşgeldiniz",
        "pickup_office": "Teslim Alma Ofisi",
        "pickup_date": "Teslim Alma Tarihi",
        "pickup_time": "Teslim Alma Saati",
        "return_office": "İade Ofisi",
        "return_date": "İade Tarihi",
        "return_time": "İade Saati",
        "rent_for_days": "Spesifik Kriterlere Göre Kirala",
        "logout": "Çıkış Yap",
        "login": "Giriş Yap",
        "register": "Kayıt Ol",
        "office_map": "Ofis Haritası",
        "no_cars_found": "Aradığınız kriterlere uygun araba bulunamadı.",
        "results": "Sonuçlar",
        "show_cars": "Arabaları Göster",
        "back_to_home": "Ana Sayfaya Dön",
        "sort_by": "Sırala",
        "transmission": "Vites Tipi",
        "cost": "Fiyat",
        "deposit": "Depozito",
        "mileage": "Kilometre",
        "age": "Yaş",
        "rental_cost": "Kiralama Ücreti",
        "filter_transmission": "Vitese Göre Filtrele",
        "all": "Tümü",
        "automatic": "Otomatik",
        "manual": "Manuel",
        "sort_order": "Sıralama Düzeni",
        "ascending": "Artan",
        "descending": "Azalan",
        "email": "E-posta",
        "password": "Şifre",
        "username": "Kullanıcı Adı",
        "country": "Ülke",
        "city": "Şehir",
        "profile_picture": "Profil Fotoğrafı",
        "profile_picture_optional": "Profil Fotoğrafı (Opsiyonel)",
        "search": "Ara",
        "select_pickup_office": "Teslim Alma Ofisi Seçin",
        "select_return_office": "İade Ofisi Seçin",
        "search_results": "Arama Sonuçları",
        "car_details": "Araç Detayları",
        "office_information": "Ofis Bilgileri",
        "phone": "Telefon",
        "home": "Ana Sayfa",
        "select_language": "Dil Seç",
        "register_now": "Hemen Kayıt Ol",
        "login_now": "Giriş Yap",
        "confirm_password": "Şifreyi Onayla",
    }
}


@app.context_processor
def inject_is_authenticated():
    return dict(is_authenticated=is_authenticated)

def create_sample_data():
    if not Office.query.first():
        # Create offices
        offices_data = [
    {
        "name": "Izmir Konak Jaybe Office",
        "location": "Izmir, Konak",
        "address": "Cumhuriyet Meydanı, Konak, İzmir",
        "phone_no": "+90 232 123 45 67",
        "latitude": 38.4237,
        "longitude": 27.1428
    },
    {
        "name": "Istanbul Beşiktaş Jaybe Office",
        "location": "Istanbul, Beşiktaş",
        "address": "Levent, Beşiktaş, İstanbul",
        "phone_no": "+90 212 345 67 89",
        "latitude": 41.0082,
        "longitude": 28.9784
    },
    {
        "name": "Ankara Çankaya Jaybe Office",
        "location": "Ankara, Çankaya",
        "address": "Kocatepe Mah., Çankaya, Ankara",
        "phone_no": "+90 312 987 65 43",
        "latitude": 39.9334,
        "longitude": 32.8597
    },
    {
        "name": "Manisa Yunusemre Jaybe Office",
        "location": "Manisa, Yunusemre",
        "address": "Atatürk Caddesi, Yunusemre, Manisa",
        "phone_no": "+90 236 123 45 67",
        "latitude": 38.6191,
        "longitude": 27.4289
    },
    {
        "name": "Balıkesir Karesi Jaybe Office",
        "location": "Balıkesir, Karesi",
        "address": "Zağnospaşa Mah., Karesi, Balıkesir",
        "phone_no": "+90 266 654 32 10",
        "latitude": 39.6484,
        "longitude": 27.8826
    },
    {
        "name": "Denizli Merkezefendi Jaybe Office",
        "location": "Denizli, Merkezefendi",
        "address": "İzmir Yolu, Merkezefendi, Denizli",
        "phone_no": "+90 258 234 56 78",
        "latitude": 37.7765,
        "longitude": 29.0864
    },
    {
        "name": "Bursa Osmangazi Jaybe Office",
        "location": "Bursa, Osmangazi",
        "address": "Bursa Caddesi, Osmangazi, Bursa",
        "phone_no": "+90 224 765 43 21",
        "latitude": 40.1826,
        "longitude": 29.0665
    },
    {
        "name": "Antalya Muratpaşa Jaybe Office",
        "location": "Antalya, Muratpaşa",
        "address": "Kazım Karabekir Caddesi, Muratpaşa, Antalya",
        "phone_no": "+90 242 456 78 90",
        "latitude": 36.8969,
        "longitude": 30.7133
    }
]


        for office_data in offices_data:
            office = Office(**office_data)
            db.session.add(office)
        db.session.commit()

        offices = Office.query.all()
        car_data = [
    {"name": "Audi A6", "transmission": "Automatic", "cost": 55000, "deposit": 8000, "mileage": 8000, "age": 2, "rental_cost": 180, "image": "images/audia6.jpg"},
    {"name": "Mercedes Benz A200", "transmission": "Manual", "cost": 45000, "deposit": 6000, "mileage": 11000, "age": 1, "rental_cost": 150, "image": "images/benza200.jpg"},
    {"name": "BMW 3", "transmission": "Automatic", "cost": 40000, "deposit": 6000, "mileage": 1000, "age": 1, "rental_cost": 120, "image": "images/bmw3.jpg"},
    {"name": "Citroen E-C4", "transmission": "Manual", "cost": 30000, "deposit": 2500, "mileage": 9000, "age": 3, "rental_cost": 80, "image": "images/citroen.png"},
    {"name": "Clio 4", "transmission": "Automatic", "cost": 31000, "deposit": 6500, "mileage": 5500, "age": 4, "rental_cost": 100, "image": "images/clio4.jpg"},
    {"name": "Fiat Linea", "transmission": "Manual", "cost": 33000, "deposit": 7700, "mileage": 10000, "age": 3, "rental_cost": 115, "image": "images/fiat-linea-araba-resimleri-2968.png"},
    {"name": "Honda Civic", "transmission": "Automatic", "cost": 30000, "deposit": 6300, "mileage": 1900, "age": 4, "rental_cost": 100, "image": "images/hondacivic.jpg"},
    {"name": "Kia Sportage", "transmission": "Manual", "cost": 27000, "deposit": 3400, "mileage": 6000, "age": 1, "rental_cost": 95, "image": "images/kia.jpg"},
    {"name": "Mazda MX-5", "transmission": "Automatic", "cost": 37000, "deposit": 5800, "mileage": 9000, "age": 3, "rental_cost": 135, "image": "images/mazda.jpg"},
    {"name": "Nissan Juke", "transmission": "Manual", "cost": 25000, "deposit": 4600, "mileage": 12500, "age": 5, "rental_cost": 95, "image": "images/nissan-juke.jpg"},
    {"name": "Peugeot 2008", "transmission": "Automatic", "cost": 31000, "deposit": 5600, "mileage": 7000, "age": 2, "rental_cost": 100, "image": "images/Peugeot2008.jpg"},
    {"name": "Toyota Corolla", "transmission": "Manual", "cost": 23000, "deposit": 4800, "mileage": 14000, "age": 3, "rental_cost": 90, "image": "images/toyota-corolla-on.jpg"},
    {"name": "Tesla 3", "transmission": "Automatic", "cost": 68000, "deposit": 9700, "mileage": 10000, "age": 1, "rental_cost": 210, "image": "images/tesla-model3.jpg"},
    {"name": "Volkswagen Golf", "transmission": "Manual", "cost": 26000, "deposit": 4900, "mileage": 8000, "age": 2, "rental_cost": 100, "image": "images/volkswagen-golf-2024.jpg"},
    {"name": "Volvo S60", "transmission": "Automatic", "cost": 44000, "deposit": 6000, "mileage": 6000, "age": 1, "rental_cost": 120, "image": "images/volvo.jpg"},
    {"name": "Hyundai i10", "transmission": "Manual", "cost": 25000, "deposit": 4700, "mileage": 13000, "age": 3, "rental_cost": 90, "image": "images/hyundai.jpg"}
]


        car_index = 0
        for office in offices:
            for _ in range(2):
                car = Car(**car_data[car_index], office_id=office.id)
                db.session.add(car)
                car_index += 1
        db.session.commit()

        print("Sample data created successfully.")

@app.before_request
def set_language():
    session.setdefault("language", "en")

@app.context_processor
def inject_language():
    lang = session.get("language", "en")
    return dict(language=lang, translations=LANGUAGES[lang])

@app.route("/set_language/<lang>")
def set_language_route(lang):
    if lang in LANGUAGES:
        session["language"] = lang
    return redirect(request.referrer or url_for("home"))

# Home page
@app.route('/')
def home():
    offices = Office.query.all()
    locations = [{"id": office.id, "lat": office.latitude, "lng": office.longitude, "name": office.name} for office in offices]
    return render_template('home.html', offices=offices, locations=locations)


@app.route('/search')
def search():
    pickup_office_id = request.args.get('pickup_office')
    pickup_date = request.args.get('pickup_date')
    pickup_time = request.args.get('pickup_time')
    return_office_id = request.args.get('return_office')
    return_date = request.args.get('return_date')
    return_time = request.args.get('return_time')
    
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'asc')  # Default to 'asc' if not provided
    filter_transmission = request.args.get('filter_transmission')
    
    # Start with all cars based on the pickup office
    cars_query = Car.query.filter_by(office_id=pickup_office_id)

    # Apply filtering by transmission if selected
    if filter_transmission:
        cars_query = cars_query.filter_by(transmission=filter_transmission)
    
    # Apply sorting based on selected criterion
    if sort_by:
        if sort_by == 'cost':
            cars_query = cars_query.order_by(Car.cost.asc() if sort_order == 'asc' else Car.cost.desc())
        elif sort_by == 'mileage':
            cars_query = cars_query.order_by(Car.mileage.asc() if sort_order == 'asc' else Car.mileage.desc())
        elif sort_by == 'age':
            cars_query = cars_query.order_by(Car.age.asc() if sort_order == 'asc' else Car.age.desc())
        elif sort_by == 'rental_cost':
            cars_query = cars_query.order_by(Car.rental_cost.asc() if sort_order == 'asc' else Car.rental_cost.desc())
        else:  # Default to sorting by transmission
            cars_query = cars_query.order_by(Car.transmission.asc() if sort_order == 'asc' else Car.transmission.desc())

    # Execute the query and get the results
    cars = cars_query.all()

    return render_template('search_results.html', cars=cars)


@app.route('/office/<int:office_id>')
def office_info(office_id):
    office = Office.query.get_or_404(office_id)
    return render_template('office_info.html', office=office)

@app.route('/office/<int:office_id>/cars')
def show_office_cars(office_id):
    office = Office.query.get_or_404(office_id)
    return render_template('search_results.html', cars=office.cars)

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password(user.password, password):
            session['user_id'] = user.id
            flash(f'Welcome, {user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        country = request.form.get('country')
        city = request.form.get('city')

        existing_user = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
        if existing_user:
            flash('Email or Username already taken.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))
        
        hashed_password = hash_password(password)

        new_user = User(
            email=email,
            username=username,
            password=hashed_password,
            country=country,
            city=city
        )

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
    app.run(debug=True)
