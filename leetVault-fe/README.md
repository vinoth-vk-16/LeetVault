# LeetVault Frontend

A modern React application for tracking your LeetCode progress through seamless GitHub integration.

## Features

- 🎨 **Beautiful UI**: Modern dark theme with animated backgrounds using WebGL shaders
- 🔐 **Google Authentication**: Secure login using Firebase Authentication
- 🚀 **React Router**: Client-side routing for seamless navigation
- 💅 **Tailwind CSS**: Utility-first CSS framework for rapid UI development
- 🎭 **Framer Motion**: Smooth animations and transitions
- 🔥 **Firebase Integration**: Backend services for authentication
- 🐙 **GitHub Integration**: Connect GitHub repos to sync LeetCode solutions
- 📊 **LeetCode Credentials**: Store and manage LeetCode session cookies

## Tech Stack

- **React 19** - UI library
- **Vite** - Build tool and dev server
- **React Router DOM** - Client-side routing
- **Firebase** - Authentication and backend services
- **Tailwind CSS** - Styling
- **Three.js** - 3D animated backgrounds
- **Framer Motion** - Animations (ethereal shadows)
- **Lucide React** - Icon library

## Project Structure

```
src/
├── components/
│   ├── ui/
│   │   ├── etheral-shadow.jsx    # Animated background component
│   │   └── login-form.jsx        # Login form with WebGL background
│   └── ProtectedRoute.jsx        # Route protection wrapper
├── pages/
│   ├── LandingPage.jsx           # Landing page with features
│   ├── LoginPage.jsx             # Login page with Google auth
│   └── HomePage.jsx              # Protected home dashboard
├── contexts/
│   └── AuthContext.jsx           # Authentication context provider
├── config/
│   └── firebase.js               # Firebase configuration
├── App.jsx                       # Main app with routing
├── main.jsx                      # App entry point
└── index.css                     # Global styles with Tailwind
```

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation

1. Clone the repository and navigate to the frontend directory:

```bash
cd leetVault-fe
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Firebase Configuration

The application uses Firebase for Google Authentication. Configuration is loaded from environment variables.

### Setup

1. Copy the example environment file:
```bash
cp env.example .env
```

2. Update `.env` with your Firebase credentials:
```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

**Firebase Project**: leetvault
- Authentication: Google Sign-In enabled
- Project ID: leetvault

## Pages

### Landing Page (`/`)
- Hero section with animated background
- Feature highlights
- Call-to-action button to get started

### Login Page (`/login`)
- Google Sign-In integration
- Beautiful WebGL animated background

### Home Page (`/home`)
- Protected route (requires authentication)
- LeetCode credentials management
- GitHub integration section
- Logout functionality

## Authentication Flow

1. User lands on the landing page
2. Clicks "Get Started" to navigate to login
3. Signs in with Google
4. Redirected to protected home page
5. Can logout to return to landing page

## GitHub Integration Flow

1. **Connect GitHub**: Click "Connect GitHub" button on home page
2. **Install App**: Redirected to GitHub to install LeetVault app
3. **Select Repositories**: Choose which repos the app can access
4. **Callback**: GitHub redirects back to home page with installation data
5. **Select Repository**: Choose one repository to activate for syncing
6. **Disconnect**: Option to disconnect and select a different repository

### API Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/check` | POST | Check/create user and get GitHub status |
| `/api/auth/github/install` | GET | Get GitHub App installation URL |
| `/api/github/installations/{id}/repositories` | GET | List available repositories |
| `/api/repos/activate` | POST | Activate a repository for syncing |
| `/api/repos/deactivate/{email}` | DELETE | Deactivate current repository |

## LeetCode Credentials

Store your LeetCode session cookie and CSRF token to enable automatic problem syncing:

1. Log in to LeetCode in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies
4. Find `LEETCODE_SESSION` and `csrftoken`
5. Copy and paste the values in the home page form

## UI Components

### DottedSurface
Three.js animated particle system creating a wave-like dotted surface background.

**Props:**
- `isDark` - Dark or light theme (boolean)
- `className` - Additional CSS classes

**Features:**
- 3D particle animation with sine wave motion
- Responsive and performant
- Automatic cleanup on unmount

### SmokeyBackground
WebGL shader-based animated background with mouse interaction for login page.

**Props:**
- `color` - Shader color (hex)
- `backdropBlurAmount` - Blur intensity
- `className` - Additional CSS classes

### LoginFormComponent
Glassmorphism-style login form with animated floating labels.

**Props:**
- `onGoogleSignIn` - Callback for Google sign-in

## Styling

The application uses Tailwind CSS with a dark theme palette:
- Primary: Blue (#3B82F6)
- Background: Black (#000000)
- Cards: Gray-900 with borders
- Accent colors: Green, Blue

## Environment

The frontend connects to the backend API at `http://localhost:8000` by default. This is configured in `HomePage.jsx`:

```javascript
const API_BASE_URL = 'http://69481ac30014e1672988.sgp.appwrite.run';
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
