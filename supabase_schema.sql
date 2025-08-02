-- Create the 'profiles' table for additional user data
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users ON DELETE CASCADE PRIMARY KEY,
  username TEXT UNIQUE,
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create the 'conversations' table
CREATE TABLE public.conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create the 'messages' table
CREATE TABLE public.messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES public.conversations(id) ON DELETE CASCADE,
  sender_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create the 'feedbacks' table
CREATE TABLE public.feedbacks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  feedback_text TEXT NOT NULL,
  rating INT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create the 'visitors' table
CREATE TABLE public.visitors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ip_address INET,
  user_agent TEXT,
  visit_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS) for each table
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.feedbacks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.visitors ENABLE ROW LEVEL SECURITY;

-- RLS Policies for 'profiles' table
CREATE POLICY "Allow individual select access" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Allow individual insert access" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "Allow individual update access" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Allow individual delete access" ON public.profiles FOR DELETE USING (auth.uid() = id);

-- RLS Policies for 'conversations' table
CREATE POLICY "Allow authenticated users to create conversations" ON public.conversations FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
CREATE POLICY "Allow users to view their own conversations" ON public.conversations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Allow users to update their own conversations" ON public.conversations FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Allow users to delete their own conversations" ON public.conversations FOR DELETE USING (auth.uid() = user_id);

-- RLS Policies for 'messages' table
CREATE POLICY "Allow authenticated users to send messages" ON public.messages FOR INSERT WITH CHECK (auth.uid() = sender_id);
CREATE POLICY "Allow users to view messages in their conversations" ON public.messages FOR SELECT USING (EXISTS (SELECT 1 FROM public.conversations WHERE id = conversation_id AND user_id = auth.uid()));
CREATE POLICY "Allow users to update their own messages" ON public.messages FOR UPDATE USING (auth.uid() = sender_id);
CREATE POLICY "Allow users to delete their own messages" ON public.messages FOR DELETE USING (auth.uid() = sender_id);

-- RLS Policies for 'feedbacks' table
CREATE POLICY "Allow authenticated users to insert feedback" ON public.feedbacks FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);
CREATE POLICY "Allow all authenticated users to view feedback" ON public.feedbacks FOR SELECT USING (auth.uid() IS NOT NULL);

-- RLS Policies for 'visitors' table
CREATE POLICY "Allow anonymous insert for visitors" ON public.visitors FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow all authenticated users to view visitors" ON public.visitors FOR SELECT USING (auth.uid() IS NOT NULL);
