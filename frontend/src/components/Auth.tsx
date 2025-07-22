"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Eye, EyeOff, Activity } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { supabase } from "../lib/supabase";
import { useNavigate } from "react-router-dom";
import api from "../lib/axios";

export default function AuthPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loginForm, setLoginForm] = useState({ email: "", password: "" });
  const [signupForm, setSignupForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");

  const { login, signup, isLoading } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      await login(loginForm.email, loginForm.password);

      // Get the user info from Supabase after login
      const {
        data: { user },
      } = await supabase.auth.getUser();

      if (user) {
        // Check if user profile exists in your DB
        const res = await api.get(`/api/users/${user.id}`);
        if (!res.data) {
          // If not, create it using metadata for first/last name
          await api.post("/api/users", {
            user_id: user.id,
            email: user.email,
            full_name: `${user.user_metadata?.firstName || ""} ${
              user.user_metadata?.lastName || ""
            }`.trim(),
            avatar_url: null,
          });
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    }
  };

  const navigate = useNavigate();

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (signupForm.password !== signupForm.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const { error } = await supabase.auth.signUp(
        {
          email: signupForm.email,
          password: signupForm.password,
          options: {
            emailRedirectTo: `${window.location.origin}/`
          }
        }
      )

      navigate("/confirm-email", { state: { email: signupForm.email } });
      /*
      // Get the user info from Supabase after signup
      const { data: { user } } = await supabase.auth.getUser()
      
      console.log("user info: " + user?.id);

      if (user) {
        // Create user profile in the database
        try {
          await api.post('/api/users', {
            user_id: user.id,
            email: user.email,
            full_name: `${signupForm.firstName} ${signupForm.lastName}`,
            avatar_url: null
          })
          console.log("User profile created successfully")
        } catch (profileError) {
          console.error("Failed to create user profile:", profileError)
          // Don't show this error to user since signup was successful
        }
      }
      */

      // Reset form after successful signup
      setSignupForm({
        firstName: "",
        lastName: "",
        email: "",
        password: "",
        confirmPassword: "",
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header Navigation */}
      <header className="border-b border-slate-700/50 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Activity className="h-6 w-6 text-orange-500" />
              <span className="text-xl font-bold text-white">
                NBA <span className="text-orange-500">IQ</span>
              </span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a
                href="#"
                className="text-orange-500 hover:text-orange-400 transition-colors"
              >
                Home
              </a>
              <a
                href="#"
                className="text-slate-300 hover:text-white transition-colors"
              >
                Match Prediction
              </a>
              <a
                href="#"
                className="text-slate-300 hover:text-white transition-colors"
              >
                MVP Analysis
              </a>
              <a
                href="#"
                className="text-slate-300 hover:text-white transition-colors"
              >
                Analytics
              </a>
              <a
                href="#"
                className="text-slate-300 hover:text-white transition-colors"
              >
                Team Comparison
              </a>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-md mx-auto">
          {/* Logo Section */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-orange-500/20 rounded-full mb-4">
              <Activity className="h-8 w-8 text-orange-500" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">
              NBA <span className="text-orange-500">IQ</span>
            </h1>
            <p className="text-slate-400">Access your analytics dashboard</p>
          </div>

          {/* Auth Forms */}
          <Card className="bg-slate-800/50 border-slate-700 backdrop-blur-sm">
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2 bg-slate-700/50">
                <TabsTrigger
                  value="login"
                  className="data-[state=active]:bg-orange-500 data-[state=active]:text-white"
                >
                  Sign In
                </TabsTrigger>
                <TabsTrigger
                  value="signup"
                  className="data-[state=active]:bg-orange-500 data-[state=active]:text-white"
                >
                  Sign Up
                </TabsTrigger>
              </TabsList>

              {/* Login Form */}
              <TabsContent value="login">
                <CardHeader className="space-y-1">
                  <CardTitle className="text-2xl text-white">
                    Welcome back
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Enter your credentials to access your account
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {error && (
                    <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-3 py-2 rounded-md text-sm">
                      {error}
                    </div>
                  )}
                  <form onSubmit={handleLogin} className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="email" className="text-slate-300">
                        Email
                      </Label>
                      <Input
                        id="email"
                        type="email"
                        placeholder="Enter your email"
                        value={loginForm.email}
                        onChange={(e) =>
                          setLoginForm({ ...loginForm, email: e.target.value })
                        }
                        className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password" className="text-slate-300">
                        Password
                      </Label>
                      <div className="relative">
                        <Input
                          id="password"
                          type={showPassword ? "text" : "password"}
                          placeholder="Enter your password"
                          value={loginForm.password}
                          onChange={(e) =>
                            setLoginForm({
                              ...loginForm,
                              password: e.target.value,
                            })
                          }
                          className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500 pr-10"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
                        >
                          {showPassword ? (
                            <EyeOff className="h-4 w-4" />
                          ) : (
                            <Eye className="h-4 w-4" />
                          )}
                        </button>
                      </div>
                    </div>
                    <div className="flex items-center justify-between">
                      <label className="flex items-center space-x-2 text-sm text-slate-300">
                        <input
                          type="checkbox"
                          className="rounded border-slate-600 bg-slate-700"
                        />
                        <span>Remember me</span>
                      </label>
                      <a
                        href="#"
                        className="text-sm text-orange-500 hover:text-orange-400"
                      >
                        Forgot password?
                      </a>
                    </div>
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full bg-orange-500 hover:bg-orange-600 text-white disabled:opacity-50"
                    >
                      {isLoading ? "Signing In..." : "Sign In"}
                    </Button>
                  </form>
                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <span className="w-full border-t border-slate-600" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                      <span className="bg-slate-800 px-2 text-slate-400">
                        Or continue with
                      </span>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <Button
                      variant="outline"
                      className="border-slate-600 bg-slate-700/50 text-slate-300 hover:bg-slate-700"
                    >
                      Google
                    </Button>
                    <Button
                      variant="outline"
                      className="border-slate-600 bg-slate-700/50 text-slate-300 hover:bg-slate-700"
                    >
                      GitHub
                    </Button>
                  </div>
                </CardContent>
              </TabsContent>

              {/* Signup Form */}
              <TabsContent value="signup">
                <CardHeader className="space-y-1">
                  <CardTitle className="text-2xl text-white">
                    Create account
                  </CardTitle>
                  <CardDescription className="text-slate-400">
                    Join NBA IQ to access advanced basketball analytics
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {error && (
                    <div className="bg-red-500/10 border border-red-500/20 text-red-400 px-3 py-2 rounded-md text-sm">
                      {error}
                    </div>
                  )}
                  <form onSubmit={handleSignup} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="firstName" className="text-slate-300">
                          First name
                        </Label>
                        <Input
                          id="firstName"
                          placeholder="John"
                          value={signupForm.firstName}
                          onChange={(e) =>
                            setSignupForm({
                              ...signupForm,
                              firstName: e.target.value,
                            })
                          }
                          className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500"
                          required
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="lastName" className="text-slate-300">
                          Last name
                        </Label>
                        <Input
                          id="lastName"
                          placeholder="Doe"
                          value={signupForm.lastName}
                          onChange={(e) =>
                            setSignupForm({
                              ...signupForm,
                              lastName: e.target.value,
                            })
                          }
                          className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500"
                          required
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="signupEmail" className="text-slate-300">
                        Email
                      </Label>
                      <Input
                        id="signupEmail"
                        type="email"
                        placeholder="Enter your email"
                        value={signupForm.email}
                        onChange={(e) =>
                          setSignupForm({
                            ...signupForm,
                            email: e.target.value,
                          })
                        }
                        className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500"
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label
                        htmlFor="signupPassword"
                        className="text-slate-300"
                      >
                        Password
                      </Label>
                      <div className="relative">
                        <Input
                          id="signupPassword"
                          type={showPassword ? "text" : "password"}
                          placeholder="Create a password"
                          value={signupForm.password}
                          onChange={(e) =>
                            setSignupForm({
                              ...signupForm,
                              password: e.target.value,
                            })
                          }
                          className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500 pr-10"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
                        >
                          {showPassword ? (
                            <EyeOff className="h-4 w-4" />
                          ) : (
                            <Eye className="h-4 w-4" />
                          )}
                        </button>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <Label
                        htmlFor="confirmPassword"
                        className="text-slate-300"
                      >
                        Confirm password
                      </Label>
                      <div className="relative">
                        <Input
                          id="confirmPassword"
                          type={showConfirmPassword ? "text" : "password"}
                          placeholder="Confirm your password"
                          value={signupForm.confirmPassword}
                          onChange={(e) =>
                            setSignupForm({
                              ...signupForm,
                              confirmPassword: e.target.value,
                            })
                          }
                          className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500 pr-10"
                          required
                        />
                        <button
                          type="button"
                          onClick={() =>
                            setShowConfirmPassword(!showConfirmPassword)
                          }
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
                        >
                          {showConfirmPassword ? (
                            <EyeOff className="h-4 w-4" />
                          ) : (
                            <Eye className="h-4 w-4" />
                          )}
                        </button>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        className="rounded border-slate-600 bg-slate-700"
                        required
                      />
                      <label className="text-sm text-slate-300">
                        I agree to the{" "}
                        <a
                          href="#"
                          className="text-orange-500 hover:text-orange-400"
                        >
                          Terms of Service
                        </a>{" "}
                        and{" "}
                        <a
                          href="#"
                          className="text-orange-500 hover:text-orange-400"
                        >
                          Privacy Policy
                        </a>
                      </label>
                    </div>
                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full bg-orange-500 hover:bg-orange-600 text-white disabled:opacity-50"
                    >
                      {isLoading ? "Creating Account..." : "Create Account"}
                    </Button>
                  </form>
                  <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                      <span className="w-full border-t border-slate-600" />
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                      <span className="bg-slate-800 px-2 text-slate-400">
                        Or continue with
                      </span>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <Button
                      variant="outline"
                      className="border-slate-600 bg-slate-700/50 text-slate-300 hover:bg-slate-700"
                    >
                      Google
                    </Button>
                    <Button
                      variant="outline"
                      className="border-slate-600 bg-slate-700/50 text-slate-300 hover:bg-slate-700"
                    >
                      GitHub
                    </Button>
                  </div>
                </CardContent>
              </TabsContent>
            </Tabs>
          </Card>

          {/* Footer */}
          <div className="text-center mt-8">
            <p className="text-slate-400 text-sm">
              © 2024 NBA IQ. Advanced Basketball Analytics Platform.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
