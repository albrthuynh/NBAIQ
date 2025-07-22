"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity, ArrowLeft, Shield, Eye, EyeOff } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
import { supabase } from "../lib/supabase"

export default function ResetPasswordPage() {
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isValidSession, setIsValidSession] = useState(false)

  const navigate = useNavigate()

  // Check if user has a valid reset session
  useEffect(() => {
    const checkSession = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession()
        if (session?.user) {
          setIsValidSession(true)
        } else {
          // No valid session, redirect to forgot password
          setError("Invalid or expired reset link. Please request a new one.")
          setTimeout(() => {
            navigate("/forgot-password")
          }, 3000)
        }
      } catch (err) {
        setError("Unable to verify reset session. Please try again.")
        setTimeout(() => {
          navigate("/forgot-password")
        }, 3000)
      }
    }

    checkSession()
  }, [navigate])

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    
    if (password !== confirmPassword) {
      setError("Passwords do not match")
      setIsLoading(false)
      return
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters")
      setIsLoading(false)
      return
    }

    try {
      const { error } = await supabase.auth.updateUser({ 
        password: password 
      })

      if (error) {
        setError(error.message || "Failed to reset password")
      } else {
        setSuccess("Password reset successfully! Redirecting to login...")
        // Redirect to login after successful reset
        setTimeout(() => {
          navigate("/")
        }, 2000)
      }
    } catch (err) {
      setError("An unexpected error occurred. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  // Show loading while checking session
  if (!isValidSession && !error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Verifying reset link...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Header Navigation */}
      <header className="border-b border-slate-700/50 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-2">
              <Activity className="h-6 w-6 text-orange-500" />
              <span className="text-xl font-bold text-white">
                NBA <span className="text-orange-500">IQ</span>
              </span>
            </Link>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-16">
        <div className="max-w-md mx-auto">
          {/* Back to Login */}
          <div className="mb-6">
            <Link
              to="/forgot-password"
              className="inline-flex items-center space-x-2 text-slate-400 hover:text-orange-400 transition-colors"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Forgot Password</span>
            </Link>
          </div>

          {/* Logo Section */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-orange-500/20 rounded-full mb-4">
              <Shield className="h-8 w-8 text-orange-500" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Reset Password
            </h1>
            <p className="text-slate-400">
              Enter your new password below
            </p>
          </div>

          {/* Success Message */}
          {success && (
            <div className="mb-4 p-4 bg-green-500/10 border border-green-500/20 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                <p className="text-green-400 text-sm font-medium">{success}</p>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-4 p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-red-400 rounded-full"></div>
                <p className="text-red-400 text-sm font-medium">{error}</p>
              </div>
            </div>
          )}

          {/* Password Reset Form */}
          <Card className="bg-slate-800/50 border-slate-700 backdrop-blur-sm">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl text-white">Set new password</CardTitle>
              <CardDescription className="text-slate-400">
                Your new password must be different from previous passwords
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleResetPassword} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="newPassword" className="text-slate-300">
                    New password
                  </Label>
                  <div className="relative">
                    <Input
                      id="newPassword"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter new password"
                      value={password}
                      className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500 pr-10"
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="confirmNewPassword" className="text-slate-300">
                    Confirm new password
                  </Label>
                  <div className="relative">
                    <Input
                      id="confirmNewPassword"
                      type={showConfirmPassword ? "text" : "password"}
                      placeholder="Confirm new password"
                      value={confirmPassword}
                      className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500 pr-10"
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-300"
                    >
                      {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                </div>
                <div className="bg-slate-700/30 p-3 rounded-lg">
                  <p className="text-xs text-slate-400 mb-2">Password must contain:</p>
                  <ul className="text-xs text-slate-400 space-y-1">
                    <li>• At least 8 characters</li>
                    <li>• One uppercase letter</li>
                    <li>• One lowercase letter</li>
                    <li>• One number</li>
                  </ul>
                </div>
                <Button
                  type="submit"
                  className="w-full bg-orange-500 hover:bg-orange-600 text-white"
                  disabled={isLoading || !isValidSession}
                >
                  {isLoading ? "Resetting..." : "Reset Password"}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Footer */}
          <div className="text-center mt-8">
            <p className="text-slate-400 text-sm">© 2024 NBA IQ. Advanced Basketball Analytics Platform.</p>
          </div>
        </div>
      </main>
    </div>
  )
}
