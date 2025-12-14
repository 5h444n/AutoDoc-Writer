import React from 'react';
import { Github, Loader2 } from 'lucide-react';

// Define the component's props using TypeScript interface
interface GitHubLoginButtonProps {
  isLoading: boolean;
  onClick: () => void;
}

const GitHubLoginButton: React.FC<GitHubLoginButtonProps> = ({ isLoading, onClick }) => {
  return (
    <button
      onClick={onClick}
      disabled={isLoading}
      // Tailwind CSS Classes: All classes must be within this single string, 
      // ensuring the button has hover, focus, and disabled states.
      className="group relative w-full flex justify-center py-3 px-4 
                 border border-transparent text-sm font-medium rounded-md 
                 text-white bg-[#24292e] 
                 hover:bg-black 
                 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 
                 transition-all duration-200 
                 disabled:opacity-70 disabled:cursor-not-allowed" // <-- এইখানে অবশ্যই ক্লোজিং কোটেশন (") থাকতে হবে
    >
      {isLoading ? (
        // Loading State UI
        <div className="flex items-center">
          <Loader2 className="animate-spin h-5 w-5 mr-2" />
          Connecting...
        </div>
      ) : (
        // Default State UI
        <div className="flex items-center">
          <Github className="h-5 w-5 mr-2" />
          Login with GitHub
        </div>
      )}
    </button> // <-- এইখানে অবশ্যই ক্লোজিং ট্যাগ (</button>) থাকতে হবে
  );
};

export default GitHubLoginButton;