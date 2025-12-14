import React, { useState } from 'react';
import GitHubLoginButton from './GitHubLoginButton'; // Import the new component

const LoginScreen: React.FC = () => {
  // State to simulate the authentication process
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = () => {
    // In Sprint 1, this is a placeholder. 
    // It will eventually trigger the backend OAuth flow[cite: 172].
    console.log("Starting GitHub OAuth flow...");
    setIsLoading(true);

    // Placeholder for API call delay (Remove this in Sprint 2 when logic is implemented)
    // setTimeout(() => {
    //   setIsLoading(false);
    // }, 3000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-slate-900 px-4">
      <div className="max-w-md w-full space-y-8 text-center bg-white dark:bg-slate-800 p-10 rounded-xl shadow-lg">
        {/* Branding (from Step 2) */}
        {/* ... (Logo and Title/Tagline) ... */}

        {/* The new interactive button */}
        <GitHubLoginButton 
          isLoading={isLoading} 
          onClick={handleLogin} 
        />
        
      </div>
    </div>
  );
};

export default LoginScreen;