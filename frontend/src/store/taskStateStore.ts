import { create } from 'zustand';
import { protectedInstance } from '../util/axiosHelpers';


export type Task = {
  token: string;   
  type: 'spot' | 'visit';
  name: string; 
  status: 'pending' | 'success' | 'failed';
  progress: number;
}

type TaskState = {
  tasks: Task[];
  addTask: (token: string, type: 'spot' | 'visit', name: string) => void;
  removeTask: (token: string) => void;
  updateTask: (token: string, updates: Partial<Task>) => void;
  startPolling: () => void;
}

export const useTaskStore = create<TaskState>((set, get) => {
  let pollingInterval: number | null = null;

  return {
    tasks: [],

    addTask: (token, type, name) => {
      const newTask: Task = {
        token,
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
        tasks: state.tasks.map((t) => (t.token === id ? { ...t, ...updates } : t)),
      }));
    },

    removeTask: (id) => {
      set((state) => ({
        tasks: state.tasks.filter((t) => t.token !== id),
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
              const res = await protectedInstance.get(`/spot/status/${task.token}`)
              const { progress, state } = res.data

              if (state === 'SUCCESS') {
                updateTask(task.token, { status: 'success', progress: 100 })
                setTimeout(() => removeTask(task.token), 5000);

              } else if (state === 'FAILURE' || state === 'REVOKED') {
                updateTask(task.token, { status: 'failed' })
              }
              else if (state === 'UNKNOWN') {
                updateTask(task.token, { status: 'failed', progress: 0 })
                }     
               else {
                updateTask(task.token, { progress })
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