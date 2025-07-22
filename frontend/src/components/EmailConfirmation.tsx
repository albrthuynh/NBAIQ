import { Button } from "@/components/ui/button";
import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";
import { supabase } from "../lib/supabase";

export default function EmailConfirmation() {
  const location = useLocation();
  const email = location.state?.email || "";
  const [resent, setResent] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleResend = async () => {
    setError("");
    setResent(false);
    const { error } = await supabase.auth.resend({
      type: "signup",
      email,
    });
    if (error) setError(error.message);
    else setResent(true);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-slate-900">
      <div className="bg-slate-800 p-8 rounded shadow-md text-center">
        <h2 className="text-2xl font-bold text-white mb-4">
          Email Confirmation Required
        </h2>
        <p className="text-slate-300 mb-4">
          A confirmation email has been sent to{" "}
          <span className="text-orange-400">{email}</span>.
          <br />
          Please check your inbox and follow the link to activate your account.
        </p>
        {resent && (
          <div className="text-green-400 mb-2">Confirmation email resent!</div>
        )}
        {error && <div className="text-red-400 mb-2">{error}</div>}
        <Button onClick={handleResend} className="mb-2 w-full">
          Resend Confirmation Email
        </Button>
        <Button
          variant="outline"
          onClick={() => navigate("/")}
          className="w-full"
        >
          Back to Home/Login
        </Button>
      </div>
    </div>
  );
}
