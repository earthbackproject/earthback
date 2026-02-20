# Supabase Setup — Run These Once

## Step 1: Run the database schema

Go to your Supabase project → **SQL Editor** → paste this entire block → click **Run**

```sql
-- Profiles table (linked to Supabase Auth users)
CREATE TABLE public.profiles (
  id           UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name   TEXT,
  last_name    TEXT,
  display_name TEXT,
  tagline      TEXT,
  bio          TEXT,
  location     TEXT,
  member_type  TEXT DEFAULT 'individual',
  what_bring   TEXT,
  what_seek    TEXT,
  skills       JSONB DEFAULT '[]'::jsonb,
  earth_score  INTEGER DEFAULT 0,
  is_public    BOOLEAN DEFAULT true,
  created_at   TIMESTAMPTZ DEFAULT NOW(),
  updated_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (required for Supabase)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Anyone can read public profiles
CREATE POLICY "Public profiles are viewable by everyone"
  ON public.profiles FOR SELECT
  USING (is_public = true);

-- Users can create and update their own profile only
CREATE POLICY "Users can upsert own profile"
  ON public.profiles FOR ALL
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);
```

---

## Step 2: Configure Authentication URLs

Go to **Authentication** → **URL Configuration** and set:

- **Site URL**: `https://earthbackproject.org`
- **Redirect URLs** (click "+ Add URL"): `https://earthbackproject.org/auth-callback.html`

Click **Save**.

---

## Step 3: Confirm magic links are enabled

Go to **Authentication** → **Providers** → **Email**

Make sure:
- ✅ Enable Email Provider is ON
- ✅ Enable magic links (OTP) is ON
- ✅ Confirm email is ON (or OFF — either works, magic links bypass it anyway)

---

## That's it. Then deploy the site.

Drop the `/site/` folder into Netlify as usual. After deploy:

1. Go to `https://earthbackproject.org/join.html`
2. Sign up with your email
3. Check your inbox — you'll get a real "Sign in to Earthback" email
4. Click the link → lands on `auth-callback.html` → saves your profile → redirects to dashboard
5. On any future visit, click **Sign In** in the nav → `login.html` → email → magic link → dashboard

Your profile will be at `profile.html?id=YOUR_SUPABASE_UUID`.
