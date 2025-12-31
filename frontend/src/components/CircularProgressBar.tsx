import { useState } from 'react';

// --- THE COMPONENT (Copy this part to your app) ---

type CircularProgressParams = {
    current?: number
    total?: number
    size?: number
    strokeWidth?: number
    color?: string
}

export function CircularProgress({
  current = 1,
  total = 1,
  size = 40,
  strokeWidth = 3,
  color = "text-white"
}: CircularProgressParams) {
  const numCurrent = Number(current) || 0;
  const numTotal = Number(total) || 1;
  const center = size / 2;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const percentage = Math.min(Math.max(numCurrent / numTotal, 0), 1);
  let strokeDashoffset = circumference - percentage * circumference;
  if (isNaN(strokeDashoffset)) strokeDashoffset = 0;

  // Dynamic font size calculation (approx 25% of container size)
  const fontSize = size * 0.25;

  return (
    <div 
      className="relative flex items-center justify-center"
      style={{ width: size, height: size }}
      role="progressbar"
      aria-valuenow={numCurrent}
      aria-valuemin={1}
      aria-valuemax={numTotal}
      aria-valuetext={`${numCurrent} of ${numTotal} images`}
    >
      <svg 
        width={size} 
        height={size} 
        style={{ transform: 'rotate(-90deg)' }} 
        className="transition-all duration-300 ease-out"
      >
        {/* Track */}
        <circle cx={center} cy={center} r={radius > 0 ? radius : 0} stroke="currentColor" strokeWidth={strokeWidth} fill="transparent" className="text-white/10" />
        {/* Progress */}
        <circle cx={center} cy={center} r={radius > 0 ? radius : 0} stroke="currentColor" strokeWidth={strokeWidth} fill="transparent" strokeDasharray={circumference > 0 ? circumference : 0} strokeDashoffset={strokeDashoffset} strokeLinecap="round" className={`${color} transition-all duration-500 ease-out`} />
      </svg>
      {/* Updated Text Container: Uses dynamic fontSize instead of fixed class */}
      <div 
        className="absolute inset-0 flex items-center justify-center font-medium text-white"
        aria-hidden="true"
        style={{ fontSize: `${fontSize}px` }}
      >
        <span>{numCurrent}</span><span className="opacity-50 mx-px">/</span><span className="opacity-60">{numTotal}</span>
      </div>
    </div>
  );
}

// --- PREVIEW WRAPPER (For testing) ---
export default function CircularProgressDemo() {
  const [progress, setProgress] = useState(1);
  const total = 10;

  return (
    <div className="min-h-screen bg-neutral-900 flex flex-col items-center justify-center gap-8 p-8 text-white">
      
      {/* 1. Large Example */}
      <div className="bg-black/50 p-8 rounded-xl border border-white/10 flex flex-col items-center gap-4">
        <h3 className="text-sm font-medium text-neutral-400 uppercase tracking-widest">Live Demo</h3>
        <CircularProgress 
          current={progress} 
          total={total} 
          size={60} 
          strokeWidth={4} 
          color={progress === total ? "text-emerald-400" : "text-blue-400"} 
        />
        <div className="flex gap-4">
          <button 
            onClick={() => setProgress(Math.max(1, progress - 1))}
            className="px-3 py-1 bg-white/10 rounded hover:bg-white/20 text-xs"
          >
            Prev
          </button>
          <button 
            onClick={() => setProgress(Math.min(total, progress + 1))}
            className="px-3 py-1 bg-white/10 rounded hover:bg-white/20 text-xs"
          >
            Next
          </button>
        </div>
      </div>

      {/* 2. Context Example (Inside a mock post footer) */}
      <div className="relative w-64 h-64 bg-neutral-800 rounded-lg overflow-hidden border border-white/10 shadow-2xl">
        <img src="https://images.unsplash.com/photo-1552374196-1ab2a1c593e8?auto=format&fit=crop&w=800&q=80" className="w-full h-full object-cover opacity-50" alt="Mock" />
        <div className="absolute bottom-3 right-3">
          <CircularProgress 
            current={3} 
            total={5} 
            size={32} 
            strokeWidth={2.5} 
            color="text-white"
          />
        </div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-xs text-center px-4">
            Mock Post Context <br/> (Bottom Right Corner)
        </div>
      </div>

    </div>
  );
}