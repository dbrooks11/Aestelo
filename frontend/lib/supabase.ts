import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(process.env.DATABASE_URL!, process.env.SUPABASE_KEY_ANON!)

