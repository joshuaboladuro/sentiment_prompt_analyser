"use client";

import { motion } from "framer-motion";
import { AnimatedFace } from "./AnimatedFace";

type Label = "positive" | "neutral" | "negative";

const STYLES: Record<Label, { name: string; color: string; soft: string; ring: string }> = {
  positive: { name: "Positive", color: "#10b981", soft: "rgba(16, 185, 129, 0.08)", ring: "rgba(16, 185, 129, 0.18)" },
  neutral: { name: "Neutral", color: "#6b7280", soft: "rgba(107, 114, 128, 0.08)", ring: "rgba(107, 114, 128, 0.18)" },
  negative: { name: "Negative", color: "#ef4444", soft: "rgba(239, 68, 68, 0.08)", ring: "rgba(239, 68, 68, 0.18)" },
};

export function ResultCard({ text, label, score }: { text: string; label: Label; score: number }) {
  const style = STYLES[label];
  const pct = Math.round(score * 100);

  return (
    <div
      className="rounded-2xl border bg-white dark:bg-zinc-900 shadow-sm p-8 overflow-hidden relative"
      style={{ borderColor: style.ring }}
    >
      <div className="absolute inset-0 pointer-events-none" style={{ background: style.soft }} />
      <div className="relative flex flex-col items-center text-center">
        <AnimatedFace label={label} color={style.color} />
        <motion.div
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15 }}
          className="mt-4 text-3xl font-semibold tracking-tight"
          style={{ color: style.color }}
        >
          {style.name}
        </motion.div>
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.25 }}
          className="mt-4 w-full max-w-xs"
        >
          <div className="flex items-center justify-between text-xs text-zinc-500 mb-1.5">
            <span>Confidence</span>
            <span className="font-medium" style={{ color: style.color }}>{pct}%</span>
          </div>
          <div className="h-2 rounded-full bg-zinc-100 dark:bg-zinc-800 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${pct}%` }}
              transition={{ delay: 0.3, duration: 0.6, ease: "easeOut" }}
              className="h-full rounded-full"
              style={{ background: style.color }}
            />
          </div>
        </motion.div>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="mt-6 text-sm text-zinc-500 dark:text-zinc-400 italic max-w-md"
        >
          &ldquo;{text}&rdquo;
        </motion.p>
      </div>
    </div>
  );
}
