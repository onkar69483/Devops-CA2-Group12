import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
    'https://hdfvltjztgesvbfncjls.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkZnZsdGp6dGdlc3ZiZm5jamxzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM1MDE5MzksImV4cCI6MjA2OTA3NzkzOX0.L63r19zJrMPnzdQhrLuMKB1VkRDVMzUgWvdwfdQxuAI',
);