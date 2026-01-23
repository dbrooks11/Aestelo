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

  const fontSize = size * 0.25;

  return (
    <div 
      className="relative flex items-center justify-center pointer-events-none select-none"
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
