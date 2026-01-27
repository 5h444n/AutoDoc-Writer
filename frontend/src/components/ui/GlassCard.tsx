import { motion } from "framer-motion";

export const GlassCard = ({ children, className = "", delay = 0, onClick }: any) => (
    <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay, ease: "easeOut" }}
        onClick={onClick}
        className={`relative bg-[#0f0f0f]/60 backdrop-blur-xl border border-white/5 rounded-2xl p-6 hover:border-white/10 transition-colors ${className}`}
    >
        {children}
    </motion.div>
);
