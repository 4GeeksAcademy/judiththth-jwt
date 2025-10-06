import React, { useEffect, useState } from "react";

const backendUrl = import.meta.env.VITE_BACKEND_URL;

export const Profile = () => {
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setError("No autenticado");
      return;
    }
    fetch(`${backendUrl}/profile`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => {
        if (data.logged_in_as) {
          setUser(data.logged_in_as);
        } else {
          setError(data.msg || "Token inválido o expirado");
          localStorage.removeItem("token");
        }
      })
      .catch(() => setError("Error de red"));
  }, []);

  if (error) return <div className="alert alert-danger mt-5">{error}</div>;
  if (!user) return <div className="mt-5">Cargando...</div>;

  return (
    <div className="container mt-5">
      <h2>Perfil privado</h2>
      <p>Email autenticado: <b>{user}</b></p>
      <button className="btn btn-secondary" onClick={() => {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }}>Cerrar sesión</button>
    </div>
  );
};
