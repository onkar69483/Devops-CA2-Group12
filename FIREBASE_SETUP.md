# Firebase Authentication Setup Guide

## 🔥 **Step-by-Step Firebase Setup**

### **1. Create a Firebase Project**

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or "Add project"
3. Enter your project name (e.g., "career-compass")
4. Choose whether to enable Google Analytics (optional)
5. Click "Create project"

### **2. Enable Authentication**

1. In your Firebase project dashboard, click "Authentication" in the left sidebar
2. Click "Get started"
3. Go to the "Sign-in method" tab
4. Enable the following providers:
   - **Email/Password**: Click "Enable" and save
   - **Google**: Click "Enable", add your authorized domain, and save

### **3. Get Your Firebase Configuration**

1. In your Firebase project dashboard, click the gear icon (⚙️) next to "Project Overview"
2. Select "Project settings"
3. Scroll down to "Your apps" section
4. Click the web icon (</>)
5. Register your app with a nickname (e.g., "Career Compass Web")
6. Copy the configuration object

### **4. Set Up Environment Variables**

Create a `.env.local` file in your project root with the following content:

```env
# Firebase Configuration
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key_here
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id
```

Replace the values with your actual Firebase configuration.

### **5. Configure Authorized Domains**

1. In Firebase Console, go to Authentication > Settings
2. Add your domain to "Authorized domains":
   - For development: `localhost`
   - For production: your actual domain

### **6. Test the Authentication**

1. Run your development server: `npm run dev`
2. Open your app in the browser
3. Click "Sign In" or "Get Started"
4. Test both email/password and Google authentication

## 🔧 **Features Included**

✅ **Email/Password Authentication**
- User registration with email verification
- Secure password requirements
- Error handling and validation

✅ **Google Authentication**
- One-click Google sign-in
- Automatic user profile creation
- Seamless integration

✅ **User State Management**
- Persistent authentication state
- Loading states and error handling
- Automatic session management

✅ **Dark Mode Compatible**
- All authentication modals work with dark mode
- Consistent styling across themes

✅ **Responsive Design**
- Mobile-friendly authentication forms
- Touch-optimized buttons and inputs

## 🚀 **Next Steps**

After setting up Firebase authentication, you can:

1. **Add User Profiles**: Store additional user data in Firestore
2. **Implement Protected Routes**: Create pages only accessible to authenticated users
3. **Add Email Verification**: Require email verification for new accounts
4. **Password Reset**: Implement forgot password functionality
5. **Social Login**: Add more providers (GitHub, Facebook, etc.)

## 📝 **Important Notes**

- Never commit your `.env.local` file to version control
- The `NEXT_PUBLIC_` prefix is required for client-side access
- Firebase configuration is safe to expose in client-side code
- Always test authentication flows thoroughly before deployment

## 🆘 **Troubleshooting**

**Common Issues:**
- **"Firebase not initialized"**: Check your environment variables
- **"Domain not authorized"**: Add your domain to Firebase authorized domains
- **"Google sign-in not working"**: Ensure Google provider is enabled in Firebase
- **"Email/password not working"**: Check if Email/Password provider is enabled

For more help, check the [Firebase Documentation](https://firebase.google.com/docs/auth). 