export const GlowButton = ({ children, onClick, disabled, className = "", variant = "primary" }: any) => (
    <button
        onClick={onClick}
        disabled={disabled}
        className={`relative px-6 py-4 rounded-xl font-bold transition-all duration-300 disabled:opacity-50 disabled:shadow-none ${variant === "primary"
                ? "bg-blue-600 text-white hover:bg-blue-500 hover:shadow-[0_0_25px_rgba(37,99,235,0.4)]"
                : "bg-slate-800 text-slate-200 hover:bg-slate-700 hover:text-white"
            } ${className}`}
    >
        {children}
    </button>
);
