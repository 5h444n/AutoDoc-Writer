export const GlowButton = ({ children, onClick, disabled, className = "", variant = "primary" }: any) => (
    <button
        onClick={onClick}
        disabled={disabled}
        className={`relative px-6 py-4 rounded-xl font-bold transition-all duration-300 disabled:opacity-50 disabled:shadow-none ${variant === "primary"
            ? "bg-gradient-to-r from-indigo-600 to-violet-600 text-white hover:from-indigo-500 hover:to-violet-500 hover:shadow-[0_0_30px_rgba(99,102,241,0.6)]"
            : "bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white border border-white/5"
            } ${className}`}
    >
        {children}
    </button>
);
