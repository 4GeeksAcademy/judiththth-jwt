import React, { useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { login } from "../services/userServices.js";
import { useNavigate } from "react-router-dom";

export const LoginForm = () => {

    //declaración de estados
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    //consumo de contexto global
    const { store, dispatch } = useGlobalReducer()

    // hooks de react router para redireccionar
    const navigate = useNavigate()

    //función info del login
    async function handleSubmit(e) {
        e.preventDefault()

        let isLogged = await login(email, password);
        console.log(isLogged);
        if (isLogged) {
            dispatch({ type: 'LOGIN', payload: isLogged })
            navigate("/private")
        }


    }

    return (
        <form className="w-50 mx-auto" onSubmit={handleSubmit}>
            <div className="mb-3">
                <label htmlFor="exampleInputEmail1" className="form-label">Email</label>
                <input type="email" className="form-control" id="exampleInputEmail1" value={email} aria-describedby="emailHelp" onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div className="mb-3">
                <label htmlFor="exampleInputPassword1" className="form-label">Contraseña</label>
                <input type="password" className="form-control" value={password} id="exampleInputPassword1" onChange={(e) => setPassword(e.target.value)} />
            </div>
            <button type="submit" className="btn btn-primary mx-2">Enviar</button>
            <a href="/" className="btn btn-danger mx-2" role="button">Cancelar</a>
        </form>
    )
}; 