"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Activity, ArrowLeft, Mail } from "lucide-react"
import { Link } from "react-router-dom"
import { supabase } from "../lib/supabase"

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("")
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSendCode = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    setSuccess("")
    
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/reset-password`,
      })

      if (error) {
        setError(error.message)
      } else {
        setSuccess("Check your email for the password reset link!")
      }
    } catch (err) {
      setError("An unexpected error occurred. Please try again.")
    } finally {
      setIsLoading(false)
    }
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
              to="/"
              className="inline-flex items-center space-x-2 text-slate-400 hover:text-orange-400 transition-colors"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Sign In</span>
            </Link>
          </div>

          {/* Logo Section */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-orange-500/20 rounded-full mb-4">
              <Mail className="h-8 w-8 text-orange-500" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Forgot Password?
            </h1>
            <p className="text-slate-400">
              No worries, we'll send you reset instructions
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

          {/* Forms */}
          <Card className="bg-slate-800/50 border-slate-700 backdrop-blur-sm">
            <CardHeader className="space-y-1">
              <CardTitle className="text-2xl text-white">Reset your password</CardTitle>
              <CardDescription className="text-slate-400">
                Enter your email address and we'll send you a reset link
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSendCode} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email" className="text-slate-300">
                    Email address
                  </Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-orange-500"
                    required
                  />
                </div>
                <Button
                  type="submit"
                  className="w-full bg-orange-500 hover:bg-orange-600 text-white"
                  disabled={isLoading}
                >
                  {isLoading ? "Sending..." : "Send Reset Link"}
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
