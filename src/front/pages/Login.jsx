import React, { useState } from "react";

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const res = await fetch(`${backendUrl}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok && data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/profile"; // Redirige a ruta protegida
      } else {
        setError(data.msg || "Error de autenticación");
      }
    } catch (err) {
      setError("Error de red");
    }
  };

  return (
    <div className="container mt-5">
      <h2>Iniciar sesión</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          className="form-control mb-2"
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={e => setPassword(e.target.value)}
          className="form-control mb-2"
          required
        />
        <button type="submit" className="btn btn-primary">Entrar</button>
      </form>
      {error && <div className="alert alert-danger mt-2">{error}</div>}
    </div>
  );
};
