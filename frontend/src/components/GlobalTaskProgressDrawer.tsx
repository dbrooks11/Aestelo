import { useState, useEffect } from 'react'

import { ChevronUp, ChevronDown, X, CheckCircle, AlertTriangle, Loader2 } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTaskStore } from '../store/taskStateStore'

export default function TaskDrawer() {
  const tasks = useTaskStore((state) => state.tasks)
  const removeTask = useTaskStore((state) => state.removeTask)
  const [isOpen, setIsOpen] = useState(false)

 
  useEffect(() => {
    const hasPending = tasks.some(t => t.status === 'pending');
    if (hasPending) setIsOpen(true)
  }, [tasks.length])

  if (tasks.length === 0) return null;

  const pendingCount = tasks.filter(t => t.status === 'pending').length
  const failedCount = tasks.filter(t => t.status === 'failed').length

 
  const headerColor = failedCount > 0 
    ? 'bg-red-900/90 border-t-red-500/50 text-red-100' 
    : 'bg-neutral-800 border-t-white/10 text-neutral-200 hover:text-white'

  return (
    <div className="fixed bottom-0 right-8 z-100 w-80 shadow-2xl flex flex-col items-end">
      
      {/* THE CONTAINER (Tab + Body) */}
      <div className="w-full bg-neutral-900 border-x border-t border-white/10 rounded-t-xl overflow-hidden">
        
        {/* 1. THE PULL TAB (Header) */}
        {/* Clicking this toggles the body below */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`w-full flex items-center justify-between px-4 py-3 text-sm font-bold border-t transition-colors cursor-pointer ${headerColor}`}
        >
          <div className="flex items-center gap-2">
            {failedCount > 0 ? (
                <AlertTriangle size={16} className="text-red-400" />
            ) : pendingCount > 0 ? (
                <Loader2 size={16} className="animate-spin text-blue-400" />
            ) : (
                <CheckCircle size={16} className="text-emerald-400" />
            )}
            
            <span>
              {failedCount > 0 ? `${failedCount} Failed` : 
               pendingCount > 0 ? `${pendingCount} Uploading...` : 
               'Uploads Complete'}
            </span>
          </div>

          {/* Arrow flips based on state */}
          {isOpen ? <ChevronDown size={16}/> : <ChevronUp size={16}/>}
        </button>

        {/* 2. THE DRAWER BODY (Sliding Content) */}
        <AnimatePresence initial={false}>
          {isOpen && (
            <motion.div
              initial={{ height: 0 }}
              animate={{ height: 'auto' }}
              exit={{ height: 0 }}
              transition={{ type: 'spring', bounce: 0, duration: 0.4 }}
              className="overflow-hidden"
            >
              <div className="p-4 flex flex-col gap-3 max-h-[60vh] overflow-y-auto border-t border-white/5 bg-[#0A0A0A]">
                {tasks.map((task) => (
                  <div key={task.id} className="group flex flex-col gap-2 bg-neutral-900 p-3 rounded-lg border border-white/5 relative">
                    
                    <div className="flex justify-between items-start z-10">
                      <div className="flex-1 min-w-0 pr-2">
                        <div className="text-[10px] font-bold text-neutral-500 uppercase tracking-wider">
                          {task.type === 'spot' ? 'Creating Spot' : 'Upload'}
                        </div>
                        <div className="text-xs text-white font-medium truncate" title={task.name}>
                          {task.name}
                        </div>
                      </div>
                      
                      {/* Close Button (Always visible for finished/failed tasks) */}
                      {task.status !== 'pending' && (
                          <button 
                            onClick={(e) => { e.stopPropagation(); removeTask(task.id); }} 
                            className="text-neutral-600 hover:text-white transition-colors cursor-pointer"
                          >
                              <X size={14} />
                          </button>
                      )}
                    </div>

                    {/* Progress Bar Container */}
                    <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden mt-1">
                      <div 
                        className={`h-full transition-all duration-500 ease-out ${
                          task.status === 'success' ? 'bg-emerald-500' :
                          task.status === 'failed' ? 'bg-red-500' : 'bg-blue-500'
                        }`}
                        style={{ width: task.status === 'failed' ? '100%' : `${task.progress}%` }}
                      />
                    </div>
                    
                    {/* Error Message */}
                    {task.status === 'failed' && (
                        <p className="text-[10px] text-red-400 font-medium">Processing failed. Please retry.</p>
                    )}

                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}