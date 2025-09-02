"use client";
import Image from "next/image";
import { useState, useEffect } from "react";
import { useAuth } from "@/contexts/AuthContext";
import { signOutUser } from "@/lib/firebase";
import LoginModal from "@/components/auth/LoginModal";
import SignupModal from "@/components/auth/SignupModal";

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
  const { user, loading } = useAuth();

  useEffect(() => {
    // Check for saved dark mode preference or default to system preference
    const savedMode = localStorage.getItem('darkMode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode !== null) {
      setDarkMode(savedMode === 'true');
    } else {
      setDarkMode(prefersDark);
    }
  }, []);

  useEffect(() => {
    // Apply dark mode class to document
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    // Save preference to localStorage
    localStorage.setItem('darkMode', darkMode.toString());
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleSignOut = async () => {
    await signOutUser();
  };

  const openLoginModal = () => {
    setShowLoginModal(true);
    setShowSignupModal(false);
  };

  const openSignupModal = () => {
    setShowSignupModal(true);
    setShowLoginModal(false);
  };

  const closeModals = () => {
    setShowLoginModal(false);
    setShowSignupModal(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen transition-colors duration-300 ${
      darkMode 
        ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900' 
        : 'bg-gradient-to-br from-blue-50 via-white to-purple-50'
    }`}>
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
            <span className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
              Career Compass
            </span>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className={`${darkMode ? 'text-gray-300 hover:text-blue-400' : 'text-gray-600 hover:text-blue-600'} transition-colors`}>
              Features
            </a>
            <a href="#careers" className={`${darkMode ? 'text-gray-300 hover:text-blue-400' : 'text-gray-600 hover:text-blue-600'} transition-colors`}>
              Careers
            </a>
            <a href="#about" className={`${darkMode ? 'text-gray-300 hover:text-blue-400' : 'text-gray-600 hover:text-blue-600'} transition-colors`}>
              About
            </a>
            <button 
              onClick={toggleDarkMode}
              className={`p-2 rounded-lg transition-colors ${
                darkMode 
                  ? 'bg-gray-700 text-yellow-300 hover:bg-gray-600' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
              aria-label="Toggle dark mode"
            >
              {darkMode ? (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                </svg>
              )}
            </button>
            
            {user ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {user.email ? user.email[0].toUpperCase() : 'U'}
                    </span>
                  </div>
                  <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    {user.email}
                  </span>
                </div>
                <button 
                  onClick={handleSignOut}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors text-sm"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <button 
                onClick={openLoginModal}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Sign In
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-6 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className={`text-5xl md:text-6xl font-bold mb-6 ${
            darkMode ? 'text-white' : 'text-gray-900'
          }`}>
            Your <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">Career Compass</span>
          </h1>
          <p className={`text-xl md:text-2xl mb-8 leading-relaxed ${
            darkMode ? 'text-gray-300' : 'text-gray-600'
          }`}>
            Discover the perfect career path for Indian students. Get personalized course recommendations, 
            salary insights, and job market trends to navigate your professional journey.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105">
              Explore Careers
            </button>
            {!user && (
              <button 
                onClick={openSignupModal}
                className={`border-2 border-blue-600 px-8 py-4 rounded-lg text-lg font-semibold transition-all ${
                  darkMode 
                    ? 'text-blue-400 border-blue-400 hover:bg-blue-400 hover:text-gray-900' 
                    : 'text-blue-600 hover:bg-blue-600 hover:text-white'
                }`}
              >
                Get Started
              </button>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className={`py-20 transition-colors duration-300 ${
        darkMode ? 'bg-gray-800' : 'bg-white'
      }`}>
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className={`text-4xl font-bold mb-4 ${
              darkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Why Choose Career Compass?
            </h2>
            <p className={`text-xl max-w-2xl mx-auto ${
              darkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Everything you need to make informed career decisions, tailored for the Indian job market.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className={`text-center p-6 rounded-xl transition-all hover:shadow-lg ${
              darkMode 
                ? 'bg-gradient-to-br from-gray-700 to-gray-600 hover:shadow-gray-900/50' 
                : 'bg-gradient-to-br from-blue-50 to-purple-50'
            }`}>
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className={`text-xl font-semibold mb-2 ${
                darkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Smart Career Discovery
              </h3>
              <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
                AI-powered recommendations based on your skills, interests, and the Indian job market.
              </p>
            </div>

            <div className={`text-center p-6 rounded-xl transition-all hover:shadow-lg ${
              darkMode 
                ? 'bg-gradient-to-br from-gray-700 to-gray-600 hover:shadow-gray-900/50' 
                : 'bg-gradient-to-br from-green-50 to-blue-50'
            }`}>
              <div className="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className={`text-xl font-semibold mb-2 ${
                darkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Course Recommendations
              </h3>
              <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
                Curated learning paths with top courses from Indian and international platforms.
              </p>
            </div>

            <div className={`text-center p-6 rounded-xl transition-all hover:shadow-lg ${
              darkMode 
                ? 'bg-gradient-to-br from-gray-700 to-gray-600 hover:shadow-gray-900/50' 
                : 'bg-gradient-to-br from-purple-50 to-pink-50'
            }`}>
              <div className="w-16 h-16 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className={`text-xl font-semibold mb-2 ${
                darkMode ? 'text-white' : 'text-gray-900'
              }`}>
                Salary Insights
              </h3>
              <p className={darkMode ? 'text-gray-300' : 'text-gray-600'}>
                Real-time salary data and growth projections for careers in India.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Careers Section */}
      <section id="careers" className={`py-20 transition-colors duration-300 ${
        darkMode ? 'bg-gray-900' : 'bg-gray-50'
      }`}>
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className={`text-4xl font-bold mb-4 ${
              darkMode ? 'text-white' : 'text-gray-900'
            }`}>
              Popular Career Paths
            </h2>
            <p className={`text-xl ${
              darkMode ? 'text-gray-300' : 'text-gray-600'
            }`}>
              Explore trending careers that are in high demand in India
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: "Software Engineer", salary: "₹8-25 LPA", growth: "High", color: "blue" },
              { title: "Data Scientist", salary: "₹10-30 LPA", growth: "Very High", color: "green" },
              { title: "Product Manager", salary: "₹12-35 LPA", growth: "High", color: "purple" },
              { title: "UX Designer", salary: "₹6-20 LPA", growth: "High", color: "pink" },
              { title: "DevOps Engineer", salary: "₹8-22 LPA", growth: "Very High", color: "orange" },
              { title: "AI/ML Engineer", salary: "₹12-40 LPA", growth: "Very High", color: "indigo" },
              { title: "Digital Marketing", salary: "₹4-15 LPA", growth: "Medium", color: "teal" },
              { title: "Business Analyst", salary: "₹6-18 LPA", growth: "High", color: "red" }
            ].map((career, index) => (
              <div key={index} className={`rounded-xl p-6 hover:shadow-lg transition-all transform hover:-translate-y-1 ${
                darkMode ? 'bg-gray-800 hover:shadow-gray-900/50' : 'bg-white'
              }`}>
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center mb-4 ${
                  darkMode ? 'bg-gray-700' : `${career.color}-100`
                }`}>
                  <div className={`w-6 h-6 rounded ${
                    darkMode ? 'bg-blue-500' : `${career.color}-600`
                  }`}></div>
                </div>
                <h3 className={`text-lg font-semibold mb-2 ${
                  darkMode ? 'text-white' : 'text-gray-900'
                }`}>
                  {career.title}
                </h3>
                <p className={`mb-2 ${
                  darkMode ? 'text-gray-300' : 'text-gray-600'
                }`}>
                  Avg. Salary: {career.salary}
                </p>
                <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${
                  career.growth === 'Very High' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' :
                  career.growth === 'High' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' :
                  'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                }`}>
                  {career.growth} Growth
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Navigate Your Career?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of Indian students who have found their perfect career path with Career Compass.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {user ? (
              <button className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors">
                Start Your Journey
              </button>
            ) : (
              <>
                <button 
                  onClick={openSignupModal}
                  className="bg-white text-blue-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-gray-100 transition-colors"
                >
                  Start Your Journey
                </button>
                <button 
                  onClick={openLoginModal}
                  className="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
                >
                  Sign In
                </button>
              </>
            )}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">C</span>
                </div>
                <span className="text-xl font-bold">Career Compass</span>
              </div>
              <p className="text-gray-400">
                Your trusted guide to career success in India.
              </p>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Features</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Career Discovery</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Course Recommendations</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Salary Insights</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Job Market Trends</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Resources</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Career Guide</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Interview Prep</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Resume Builder</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Success Stories</a></li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Connect</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Career Compass. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Authentication Modals */}
      <LoginModal 
        isOpen={showLoginModal} 
        onClose={closeModals} 
        onSwitchToSignup={openSignupModal}
      />
      <SignupModal 
        isOpen={showSignupModal} 
        onClose={closeModals} 
        onSwitchToLogin={openLoginModal}
      />
    </div>
  );
}
