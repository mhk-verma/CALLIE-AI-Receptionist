# CALLIE - AI Receptionist

<div align="center">

![CALLIE Logo](https://img.shields.io/badge/CALLIE-AI%20Receptionist-6366F1?style=for-the-badge&logo=python&logoColor=white)

**Your AI Receptionist, Available 24/7**

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

A production-grade AI receptionist SaaS application for small businesses. Callie answers calls, handles customer messages, answers FAQs, detects urgent issues, and never misses an important customer again.

</div>

## 🌟 Features

### Core Capabilities
- **AI Phone Receptionist** - Intelligent voice assistant that answers calls using natural language understanding
- **24/7 Availability** - Never miss a call or message, even outside business hours
- **Smart Message Handling** - Unified management of SMS, WhatsApp, Instagram DMs, and website chat
- **Automatic FAQ Answers** - Configure FAQs and let AI handle common questions automatically
- **Urgent Issue Detection** - Automatically detect and escalate urgent situations to human staff
- **Conversation History** - Complete history with AI-generated summaries and insights
- **Analytics Dashboard** - Comprehensive analytics on call volume, resolution rates, and customer intents
- **Demo Mode** - Fully functional demo mode without requiring external API credentials

### Technical Features
- **Multi-tenant Architecture** - Designed for SaaS with proper data isolation
- **Role-Based Access Control** - Owner, Staff, and Admin roles with appropriate permissions
- **REST API** - Complete REST API using Django REST Framework
- **Webhook Integration** - Secure webhook handling for Twilio and other services
- **Background Processing** - Celery for async task processing
- **Docker Support** - Complete Docker and Docker Compose setup
- **Production Ready** - Gunicorn, Nginx, PostgreSQL, Redis configuration

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 15+
- Redis 7+
- Docker and Docker Compose (optional but recommended)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai_receptionist
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Set up the database**
```bash
python manage.py migrate
```

6. **Create a superuser**
```bash
python manage.py createsuperuser
```

7. **Seed demo data**
```bash
python manage.py seed_demo_data
```

8. **Run the development server**
```bash
python manage.py runserver
```

9. **Access the application**
- Open http://localhost:8000 in your browser
- Demo credentials: `demo@example.com` / `demo123`

### Docker Setup

```bash
# Build and start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Seed demo data
docker-compose exec web python manage.py seed_demo_data
```

## 📁 Project Structure

```
ai_receptionist/
├── config/                 # Django configuration
│   ├── settings/           # Settings modules
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── apps/                   # Django applications
│   ├── accounts/           # User authentication and management
│   ├── businesses/         # Business profile and configuration
│   ├── receptionist/       # AI receptionist configuration
│   ├── calls/              # Call management
│   ├── messages/           # Message management
│   ├── contacts/           # Contact/CRM management
│   ├── conversations/       # Conversation tracking
│   ├── knowledge/          # FAQs and knowledge base
│   ├── notifications/      # Notification system
│   ├── analytics/          # Analytics and reporting
│   ├── integrations/       # Third-party integrations
│   └── demo/               # Demo mode functionality
├── services/               # Business logic services
│   ├── ai/                 # AI/LLM service abstraction
│   ├── voice/              # Voice/Twilio services
│   ├── notifications/      # Email/notification services
│   └── integrations/       # Integration services
├── templates/              # Django templates
│   ├── base.html           # Base template with layout
│   ├── components/         # Reusable components
│   ├── landing/            # Public landing page
│   ├── accounts/           # Authentication pages
│   ├── dashboard/          # Dashboard
│   ├── calls/              # Call pages
│   ├── messages/           # Message pages
│   ├── contacts/           # Contact pages
│   ├── knowledge/          # Knowledge base pages
│   ├── analytics/          # Analytics pages
│   └── demo/               # Demo pages
├── static/                 # Static files
│   └── css/                # Custom CSS (design system)
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🎨 Design System

### Color Palette
- **Primary**: Indigo `#6366F1`
- **Accent**: Cyan `#22D3EE`
- **Background**: Deep Navy `#0B1120`
- **Card**: `#172033`
- **Border**: `#263449`
- **Text**: `#F8FAFC`
- **Success**: `#10B981`
- **Warning**: `#F59E0B`
- **Urgent**: `#F97316`
- **Error**: `#EF4444`

### Typography
- **Font**: Inter / Plus Jakarta Sans
- **Page Title**: 32px / 700
- **Section Title**: 20-24px / 600
- **Body**: 14px
- **Secondary**: 13px

### Components
- **Cards** - Rounded corners (8-12px), subtle borders, minimal shadows
- **Buttons** - Primary, Secondary, Ghost, Danger variants
- **Badges** - Status indicators with semantic colors
- **Forms** - Clean inputs with focus states
- **Tables** - Responsive with proper spacing

## 🔧 Configuration

### Environment Variables

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ai_receptionist
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# AI/LLM
OPENAI_API_KEY=your-openai-api-key
AI_PROVIDER=openai  # or 'demo' for demo mode

# Twilio
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# Demo Mode
DEMO_MODE=True  # Set to False to use real APIs
```

## 🤖 AI Service Architecture

### AI Providers
The application uses an abstraction layer to support multiple AI providers:

1. **OpenAI Provider** - Uses GPT-3.5-turbo for production
2. **Demo AI Provider** - Simulates AI responses for testing without API keys

### Switching Providers
```python
# Automatically selected based on configuration
from services.ai.llm_service import get_llm_provider

llm = get_llm_provider()  # Returns OpenAI or Demo provider
```

### AI Capabilities
- **Response Generation** - Context-aware responses based on business knowledge
- **Intent Classification** - Classifies customer intents (hours, appointment, pricing, etc.)
- **Urgency Detection** - Detects urgent situations and emergency keywords
- **Conversation Summarization** - Generates AI summaries of conversations

## 📞 Voice Integration

### Twilio Setup
1. Create a Twilio account
2. Configure webhook URL to point to `/api/webhooks/twilio/voice/`
3. Set up phone number and configure voice webhook

### Demo Voice Service
The demo voice service simulates Twilio functionality without requiring credentials, perfect for demonstrations and testing.

## 🔐 Security

### Implemented Security Measures
- **CSRF Protection** - Enabled by default in Django
- **Password Hashing** - Using Django's secure password hashing
- **Environment Variables** - Sensitive data stored in environment, not in code
- **Input Validation** - Django ORM protects against SQL injection
- **XSS Protection** - Django's XSS protection enabled
- **Secure Cookies** - Configurable secure cookie settings
- **Webhook Validation** - Signature validation for external webhooks
- **Rate Limiting** - django-ratelimit for API protection
- **Role-Based Access** - Proper permission checks throughout

### Best Practices
- Never commit `.env` file or secrets to version control
- Use strong secret keys in production
- Enable HTTPS in production
- Keep dependencies updated
- Regular security audits

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/accounts/tests.py
```

### Test Structure
```
tests/
├── conftest.py           # Pytest configuration
├── test_accounts.py       # Account tests
├── test_businesses.py     # Business tests
├── test_calls.py          # Call tests
└── test_ai_service.py     # AI service tests
```

## 📊 Analytics

### Available Metrics
- **Call Volume** - Total calls, answered, missed
- **Message Volume** - Total messages by channel
- **AI Resolution Rate** - Percentage of conversations resolved by AI
- **Escalation Rate** - Percentage requiring human intervention
- **Customer Intents** - Most common customer questions
- **Channel Distribution** - Messages by platform (SMS, WhatsApp, etc.)
- **Urgency Detection** - Urgent conversations breakdown

## 🎓 Demo Mode

### What Demo Mode Does
- Simulates AI responses without requiring OpenAI API keys
- Simulates Twilio voice functionality
- Creates realistic conversation data
- Tests urgency detection and escalation
- Perfect for college presentations and demonstrations

### Using Demo Mode
1. Set `DEMO_MODE=True` in `.env`
2. Access the Live Demo page
3. Simulate calls and messages
4. View results in dashboard and analytics

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure production database
- [ ] Set up Redis for Celery
- [ ] Configure email backend
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Configure CORS properly
- [ ] Use Gunicorn as WSGI server
- [ ] Set up Nginx reverse proxy
- [ ] Configure proper static file serving
- [ ] Set up monitoring and error tracking

### Docker Deployment
```bash
# Build production image
docker build -t ai-receptionist:latest .

# Run with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 API Documentation

### Authentication
All API endpoints require authentication. Use session authentication or token authentication.

### Key Endpoints

#### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration

#### Dashboard
- `GET /api/dashboard/` - Dashboard statistics

#### Calls
- `GET /api/calls/` - List calls
- `GET /api/calls/<id>/` - Call details

#### Messages
- `GET /api/messages/` - List messages
- `GET /api/messages/<id>/` - Message details

#### Contacts
- `GET /api/contacts/` - List contacts
- `POST /api/contacts/` - Create contact
- `PUT /api/contacts/<id>/` - Update contact
- `DELETE /api/contacts/<id>/` - Delete contact

#### Knowledge
- `GET /api/knowledge/faqs/` - List FAQs
- `POST /api/knowledge/faqs/` - Create FAQ
- `PUT /api/knowledge/faqs/<id>/` - Update FAQ
- `DELETE /api/knowledge/faqs/<id>/` - Delete FAQ

#### Demo
- `POST /api/demo/simulate-call/` - Simulate call
- `POST /api/demo/simulate-message/` - Simulate message

#### Webhooks
- `POST /api/webhooks/twilio/voice/` - Twilio voice webhook
- `POST /api/webhooks/twilio/status/` - Twilio status callback
- `POST /api/webhooks/messages/` - Generic message webhook

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Django** - The web framework for perfectionists with deadlines
- **OpenAI** - GPT models for AI capabilities
- **Twilio** - Voice and messaging APIs
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide Icons** - Beautiful icon library

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

<div align="center">

**Built with ❤️ for small businesses**

CALLIE - Your AI Receptionist, Available 24/7

</div>
