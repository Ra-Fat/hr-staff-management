"use client";
import {
  decodeJwt,
  getAccessToken,
  isExpired,
  saveSession,
  userFromToken,
} from "@/src/lib/session";
import { authApi } from "@/src/services/auth";
import { ApiError } from "@/src/types/api.type";
import { Eye, EyeOff, Loader2 } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

export default function Login() {
  return (
    <div className="min-h-screen w-full bg-background flex items-center justify-center p-6">
      <div className="w-full max-w-250 bg-white rounded-2xl overflow-hidden flex flex-col lg:flex-row min-h-130">
        {/* Left — form */}
        <div className="flex-1 flex flex-col justify-center items-center px-8 sm:px-12">
          <div className="w-full">
            <h1 className="text-3xl font-semibold">Welcome back</h1>
            <p className="mt-2 text-sm text-muted">
              Enter your email and password to access your account.
            </p>
            <LoginForm />
          </div>
        </div>
        <div className="hidden lg:flex lg:w-[46%] relative bg-primary items-center justify-center p-10">
          <div
            className="absolute inset-6 rounded-2xl border-2 border-dashed border-border
              flex flex-col items-center justify-center gap-2"
          >
            <span className="text-accent text-sm font-medium">
              Image placeholder
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

function LoginForm() {
  const [showPassword, setShowPassword] = useState(false);
  // const setCurrentUser = useAppStore((s) => s.setCurrentUser);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const searchParams = useSearchParams();
  const router = useRouter();

  useEffect(() => {
    const token = getAccessToken();
    if (token && !isExpired(decodeJwt(token))) {
      router.replace(searchParams.get("redirect") ?? "/dashboard");
    }
  }, [router, searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const tokens = await authApi.login(email, password);
      saveSession(tokens.access_token, tokens.refresh_token);

      const user = userFromToken(tokens.access_token);
      try {
        const profile = await authApi.me();
        if (user) {
          user.name = profile.full_name || user.name;
          user.email = profile.email;
          user.role = profile.role?.name ?? user.role;
        }
      } catch {}
      // setCurrentUser(user);
      const redirect = searchParams.get("redirect") ?? "/dashboard";
      router.push(redirect);
    } catch (error) {
      const msg =
        error instanceof ApiError
          ? error.message
          : "Unable to sign in. Please try again";
      setError(msg);
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-10 space-y-5">
      <div className="flex flex-col gap-2">
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="email"
          placeholder="you@company.com"
          className="w-full h-12 px-4 rounded-xl border border-border"
        />
      </div>

      <div className="flex flex-col gap-2">
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <div className="relative">
          <input
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type={showPassword ? "text" : "password"}
            autoComplete="current-password"
            placeholder="••••••••••"
            className="w-full h-12 px-4 rounded-xl border border-border"
          />
          <button
            type="button"
            onClick={() => setShowPassword((v) => !v)}
            className="absolute cursor-pointer right-3.5 top-1/2 -translate-y-1/2 text-muted"
            aria-label={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
          </button>
        </div>
      </div>

      <div className="flex items-center justify-between pt-2">
        <label className="flex items-center gap-2.5 cursor-pointer select-none">
          <input type="checkbox" className="h-4 w-4 rounded border-border" />
          <span className="text-[14px] text-muted">Remember me</span>
        </label>
        <a
          href="#"
          className="text-[14px] font-medium text-primary hover:text-[#4338CA] transition-colors"
        >
          Forgot your password?
        </a>
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full h-12 bg-primary rounded-xl text-white text-md hover:bg-accent-foreground font-bold cursor-pointer"
      >
        {loading ? "Signing in..." : "Log in"}
      </button>
      {error && (
        <div className="bg-red-50 border border-red-100 text-[#EF4444] text-sm rounded-lg px-3 py-2.5">
          {error}
        </div>
      )}
    </form>
  );
}
