import { motion } from "framer-motion";

export const GlassCard = ({ children, className = "", delay = 0, onClick }: any) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay, ease: "easeOut" }}
        onClick={onClick}
        className={`relative bg-slate-900/40 backdrop-blur-xl border border-white/10 rounded-2xl p-6 hover:border-white/20 transition-colors ${className}`}
    >
        {children}
    </motion.div>
);
