"use client";
import { Eye, EyeOff } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export default function Login() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="min-h-screen w-full bg-background flex items-center justify-center p-6">
      <div className="w-full max-w-250 bg-white rounded-2xl overflow-hidden flex flex-col lg:flex-row min-h-130">
        {/* Left — form */}
        <div className="flex-1 flex flex-col justify-center items-center px-8 sm:px-12">
          <div className="w-full">
            <h1 className="text-3xl font-semibold">
              Welcome back
            </h1>
            <p className="mt-2 text-sm text-muted">
              Enter your email and password to access your account.
            </p>

            <form className="mt-10 space-y-5">
              <div className="flex flex-col gap-2">
                <label
                  htmlFor="email"
                  className="block text-sm font-medium"
                >
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  autoComplete="email"
                  placeholder="you@company.com"
                  className="w-full h-12 px-4 rounded-xl border border-border"
                />
              </div>

              <div className="flex flex-col gap-2">
                <label
                  htmlFor="password"
                  className="block text-sm font-medium"
                >
                  Password
                </label>
                <div className="relative">
                  <input
                    id="password"
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
                  <input
                    type="checkbox"
                    className="h-4 w-4 rounded border-border"
                  />
                  <span className="text-[14px] text-muted">
                    Remember me
                  </span>
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
                className="w-full h-12 bg-primary rounded-xl text-white text-md hover:bg-accent-foreground font-bold cursor-pointer"
              >
                Log in
              </button>
            </form>
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