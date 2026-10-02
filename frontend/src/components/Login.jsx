import { useState } from "react";

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username,
            password,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Invalid username or password");
      }

      const user = await response.json();
      onLogin(user);
    } catch (error) {
      setError(error.message);
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>InfraSense</h1>
        <p>Infrastructure Monitoring Login</p>

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(event) =>
            setUsername(event.target.value)
          }
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) =>
            setPassword(event.target.value)
          }
          required
        />

        {error && (
          <div className="login-error">
            {error}
          </div>
        )}

        <button type="submit">Login</button>

        <div className="demo-accounts">
          <small>Admin: admin / admin123</small>
          <small>Engineer: engineer / engineer123</small>
          <small>Viewer: viewer / viewer123</small>
        </div>
      </form>
    </div>
  );
}

export default Login;