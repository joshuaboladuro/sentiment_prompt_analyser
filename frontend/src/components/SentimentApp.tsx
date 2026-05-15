"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ResultCard } from "./ResultCard";

type Label = "positive" | "neutral" | "negative";

interface Result {
  text: string;
  label: Label;
  score: number;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export function SentimentApp() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyse = async () => {
    if (!text.trim() || loading) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/analyse`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) throw new Error(`API returned ${res.status}`);
      const data = (await res.json()) as Result;
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not reach the API. Is the backend running?",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-sm p-6">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) analyse();
          }}
          placeholder="Type a sentence... e.g. Honestly, the food was incredible."
          rows={4}
          className="w-full resize-none bg-transparent text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 focus:outline-none text-lg leading-relaxed"
          autoFocus
        />
        <div className="flex items-center justify-between mt-4 pt-4 border-t border-zinc-100 dark:border-zinc-800">
          <span className="text-xs text-zinc-400">{text.length}/2000</span>
          <button
            onClick={analyse}
            disabled={!text.trim() || loading}
            className="px-5 py-2 rounded-lg bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-medium text-sm hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition"
          >
            {loading ? "Analysing..." : "Analyse"}
          </button>
        </div>
      </div>

      <AnimatePresence mode="wait">
        {error && (
          <motion.div
            key="error"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="rounded-xl border border-red-200 bg-red-50 dark:bg-red-950 dark:border-red-900 p-4 text-sm text-red-700 dark:text-red-300"
          >
            {error}
          </motion.div>
        )}
        {result && (
          <motion.div
            key={result.text + result.label}
            initial={{ opacity: 0, y: 16, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.98 }}
            transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
          >
            <ResultCard text={result.text} label={result.label} score={result.score} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
