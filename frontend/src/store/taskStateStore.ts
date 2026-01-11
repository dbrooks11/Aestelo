import { create } from 'zustand';
import { protectedInstance } from '../util/axios_api_helpers';


export type Task = {
  id: string;   
  type: 'spot' | 'visit';
  name: string; 
  status: 'pending' | 'success' | 'failed';
  progress: number;
}

type TaskState = {
  tasks: Task[];
  addTask: (id: string, type: 'spot' | 'visit', name: string) => void;
  removeTask: (id: string) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
  startPolling: () => void;
}

export const useTaskStore = create<TaskState>((set, get) => {
  let pollingInterval: number | null = null;

  return {
    tasks: [],

    addTask: (id, type, name) => {
      const newTask: Task = {
        id,
        type,
        name,
        status: 'pending', 
        progress: 0       
      };

      set((state) => ({ tasks: [...state.tasks, newTask] }));
      get().startPolling(); 
    },

    updateTask: (id, updates) => {
      set((state) => ({
        tasks: state.tasks.map((t) => (t.id === id ? { ...t, ...updates } : t)),
      }));
    },

    removeTask: (id) => {
      set((state) => ({
        tasks: state.tasks.filter((t) => t.id !== id),
      }));
    },

    cleanTask: () => {
        set(state => ({
            tasks: state.tasks.map(t => 
                t.status === 'pending' ? { ...t, status: 'failed' } : t
            )
        }))
    },

    startPolling: () => {
      if (pollingInterval) return;

      pollingInterval = setInterval(async () => {
        const { tasks, updateTask, removeTask } = get()
        const pendingTasks = tasks.filter((t) => t.status === 'pending')

        if (pendingTasks.length === 0) {
            if (pollingInterval) clearInterval(pollingInterval)
            pollingInterval = null
            return
        }

        await Promise.all(
          pendingTasks.map(async (task) => {
            try {
              const res = await protectedInstance.get(`/spot/status/${task.id}`)
              const { progress, state } = res.data

              if (state === 'SUCCESS' || progress === 100) {
                updateTask(task.id, { status: 'success', progress: 100 })
                setTimeout(() => removeTask(task.id), 5000);

              } else if (state === 'FAILURE' || state === 'REVOKED') {
                updateTask(task.id, { status: 'failed' })
              }
              else if (state === 'UNKNOWN') {
                updateTask(task.id, { status: 'failed', progress: 0 })
                }     
               else {
                updateTask(task.id, { progress })
              }
            } catch (err) {
              console.error("Polling error", err)
            }
          })
        );
      }, 2000)
    },
  };
});