import { useState, type FormEvent } from "react";
import { Link, useNavigate } from "react-router-dom";
import { GraduationCap } from "lucide-react";
import { registerUser, type RegisterData } from "../../services/authService";
import "./Auth.css";

const initialForm: RegisterData = {
  username: "",
  email: "",
  password: "",
  phone_number: "",
  university: "",
  course: "",
  year_of_study: "",
  state: "",
  country: "",
  board: "",
  preferred_language: "English",
  bio: "",
  study_goal: "",
};

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState<RegisterData>(initialForm);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;

    setForm((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setSubmitting(true);

    try {
      const response = await registerUser(form);

      setSuccess(response.message || "Registration successful!");

      setTimeout(() => {
        navigate("/login");
      }, 1200);
    } catch (err: any) {
      const data = err.response?.data;

      if (data && typeof data === "object") {
        const messages = Object.entries(data)
          .map(([field, value]) => {
            const detail = Array.isArray(value)
              ? value.join(", ")
              : String(value);

            return `${field}: ${detail}`;
          })
          .join(" | ");

        setError(messages || "Registration failed.");
      } else {
        setError("Unable to register. Please check your connection.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page register-page">
      <div className="auth-card register-card">
        <div className="auth-brand">
          <div className="auth-logo">
            <GraduationCap size={28} />
          </div>

          <h1>StudyMate<span>AI</span></h1>
          <p>Create your learning account</p>
        </div>

        <div className="auth-heading">
          <h2>Create Account</h2>
          <p>Enter your details to get started.</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="register-grid">
            {[
              ["username", "Username"],
              ["email", "Email"],
              ["password", "Password"],
              ["phone_number", "Phone Number"],
              ["university", "University"],
              ["course", "Course"],
              ["year_of_study", "Year of Study"],
              ["state", "State"],
              ["country", "Country"],
              ["board", "Board"],
            ].map(([name, label]) => (
              <div className="form-group" key={name}>
                <label>{label}</label>
                <input
                  name={name}
                  type={
                    name === "password"
                      ? "password"
                      : name === "email"
                        ? "email"
                        : "text"
                  }
                  value={form[name as keyof RegisterData] as string}
                  onChange={handleChange}
                  placeholder={`Enter ${label.toLowerCase()}`}
                  required
                />
              </div>
            ))}

            <div className="form-group">
              <label>Preferred Language</label>
              <select
                name="preferred_language"
                value={form.preferred_language}
                onChange={handleChange}
                required
              >
                <option value="English">English</option>
                <option value="Malayalam">Malayalam</option>
                <option value="Hindi">Hindi</option>
              </select>
            </div>

            <div className="form-group">
              <label>Study Goal (Optional)</label>
              <input
                name="study_goal"
                value={form.study_goal}
                onChange={handleChange}
                placeholder="Your learning goal"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Bio (Optional)</label>
            <textarea
              name="bio"
              value={form.bio}
              onChange={handleChange}
              placeholder="Tell us about yourself"
              rows={3}
            />
          </div>

          {error && <p className="auth-error">{error}</p>}
          {success && <p className="auth-success">{success}</p>}

          <button
            className="auth-submit"
            type="submit"
            disabled={submitting}
          >
            {submitting ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account?{" "}
          <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  );
}