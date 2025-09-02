# Jubair Boot House - Professional Footwear Store

A modern, responsive web application for a footwear store built with FastAPI, featuring admin management, user authentication, product catalog, and favorites system.

## 🚀 Quick Start

### Option 1: Automatic Deployment (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run complete deployment (includes database setup)
python deploy.py

# Start the application
python run.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_database.py

# Start the application
python run.py
```

## 📋 Features

- **User Authentication**: Separate admin and user login systems
- **Product Management**: Add, edit, delete products with multiple images
- **User Favorites**: Users can save favorite products
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Admin Dashboard**: Complete admin panel for managing products and users
- **Contact System**: Built-in feedback/contact form
- **Search & Filter**: Advanced product search and filtering

## 🗄️ Database

The application uses SQLite database (`jubair_boot_house.db`) with the following tables:
- `admins` - Admin users
- `users` - Regular users
- `products` - Product catalog
- `user_favourites` - User favorite products
- `sessions` - User sessions
- `feedback` - Contact form submissions

### Default Admin Credentials
- **Username**: JuberSiddique
- **Password**: Juber@708492

## 🔧 Deployment

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run deployment: `python deploy.py`
4. Start application: `python run.py`
5. Visit: http://localhost:8000

### Production Deployment
1. Ensure all dependencies are installed
2. Run `python deploy.py` to initialize database
3. Use a production WSGI server like Gunicorn with Uvicorn workers
4. Configure reverse proxy (nginx) if needed
5. Set up SSL certificates for HTTPS

## 📁 Project Structure

```
jubair_boot_house/
├── app/                    # Main application code
│   ├── main.py            # FastAPI application
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   └── routers/           # API routes
│       ├── auth.py        # Authentication routes
│       └── products.py    # Product management routes
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   ├── images/           # Static images
│   └── uploads/          # User uploaded images
├── init_database.py      # Database initialization script
├── deploy.py             # Complete deployment script
├── run.py                # Application startup script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🛠️ API Endpoints

### Public Endpoints
- `GET /` - Home page
- `GET /products/` - Product catalog
- `GET /products/{id}` - Product details
- `POST /contact` - Contact form submission

### Authentication Endpoints
- `GET /auth/login` - Admin login page
- `POST /auth/login` - Admin login
- `GET /auth/user/login` - User login page
- `POST /auth/user/login` - User login
- `GET /auth/user/signup` - User registration
- `POST /auth/user/signup` - User registration

### Admin Endpoints
- `GET /products/admin/dashboard` - Admin dashboard
- `GET /auth/admin/users` - User management
- `GET /admin/feedback` - Feedback management

## 🔒 Security Features

- Password hashing with bcrypt
- Session management
- Admin-only access to sensitive endpoints
- Input validation and sanitization
- SQL injection protection via SQLAlchemy ORM

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🎨 UI/UX Features

- Modern, clean design
- Bootstrap 5 framework
- Font Awesome icons
- Smooth animations and transitions
- Intuitive navigation
- Professional color scheme

## 🚀 Performance

- Fast SQLite database
- Optimized queries
- Static file serving
- Efficient image handling
- Minimal dependencies

## 📞 Support

For support or questions, please contact:
- **Phone**: +91 7705925627
- **Email**: jubersiddique33@gmail.com
- **Address**: Sohasa mod Tekuatar Kushinagar, UP, India

## 📄 License

This project is proprietary software for Jubair Boot House.

---

**Jubair Boot House** - Premium Footwear Store