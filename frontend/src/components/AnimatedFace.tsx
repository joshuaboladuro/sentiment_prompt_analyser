"use client";

import { motion } from "framer-motion";

type Label = "positive" | "neutral" | "negative";

export function AnimatedFace({ label, color }: { label: Label; color: string }) {
  return (
    <motion.svg
      width="120"
      height="120"
      viewBox="0 0 120 120"
      initial={{ scale: 0.7, rotate: -8, opacity: 0 }}
      animate={{ scale: 1, rotate: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 220, damping: 14 }}
    >
      <motion.circle
        cx="60"
        cy="60"
        r="54"
        fill={color}
        animate={{ scale: [1, 1.04, 1] }}
        transition={{ duration: 2.4, repeat: Infinity, ease: "easeInOut" }}
        style={{ transformOrigin: "60px 60px" }}
      />
      <Eyes label={label} />
      <Mouth label={label} />
      {label === "positive" && <Sparkles />}
      {label === "negative" && <Tear />}
    </motion.svg>
  );
}

function Eyes({ label }: { label: Label }) {
  if (label === "positive") {
    return (
      <g fill="white">
        <motion.path
          d="M 38 50 Q 44 42, 50 50"
          stroke="white"
          strokeWidth="4"
          strokeLinecap="round"
          fill="none"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        />
        <motion.path
          d="M 70 50 Q 76 42, 82 50"
          stroke="white"
          strokeWidth="4"
          strokeLinecap="round"
          fill="none"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        />
      </g>
    );
  }
  return (
    <g fill="white">
      <motion.ellipse cx="44" cy="50" rx="5" ry="6" animate={{ scaleY: [1, 0.1, 1] }} transition={{ duration: 0.25, delay: 2, repeat: Infinity, repeatDelay: 3.5 }} style={{ transformOrigin: "44px 50px" }} />
      <motion.ellipse cx="76" cy="50" rx="5" ry="6" animate={{ scaleY: [1, 0.1, 1] }} transition={{ duration: 0.25, delay: 2, repeat: Infinity, repeatDelay: 3.5 }} style={{ transformOrigin: "76px 50px" }} />
    </g>
  );
}

function Mouth({ label }: { label: Label }) {
  const paths: Record<Label, string> = {
    positive: "M 38 76 Q 60 96, 82 76",
    neutral: "M 42 80 L 78 80",
    negative: "M 38 86 Q 60 70, 82 86",
  };
  return (
    <motion.path
      d={paths[label]}
      stroke="white"
      strokeWidth="4.5"
      strokeLinecap="round"
      fill="none"
      initial={{ pathLength: 0, opacity: 0 }}
      animate={{ pathLength: 1, opacity: 1 }}
      transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
    />
  );
}

function Sparkles() {
  const positions = [
    { x: 12, y: 22, delay: 0.5 },
    { x: 102, y: 18, delay: 0.7 },
    { x: 100, y: 96, delay: 0.9 },
  ];
  return (
    <g fill="white">
      {positions.map((p, i) => (
        <motion.path
          key={i}
          d={`M ${p.x} ${p.y - 5} L ${p.x + 1.5} ${p.y - 1.5} L ${p.x + 5} ${p.y} L ${p.x + 1.5} ${p.y + 1.5} L ${p.x} ${p.y + 5} L ${p.x - 1.5} ${p.y + 1.5} L ${p.x - 5} ${p.y} L ${p.x - 1.5} ${p.y - 1.5} Z`}
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: [0, 1.2, 1], opacity: [0, 1, 1] }}
          transition={{ duration: 0.6, delay: p.delay }}
        />
      ))}
    </g>
  );
}

function Tear() {
  return (
    <motion.path
      d="M 44 62 Q 42 70, 44 76 Q 46 70, 44 62 Z"
      fill="#60a5fa"
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: [0, 1, 1, 0], y: [-6, 0, 8, 16] }}
      transition={{ duration: 2.2, delay: 0.7, repeat: Infinity, repeatDelay: 1 }}
    />
  );
}
