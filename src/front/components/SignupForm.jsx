import React, { useEffect, useState } from "react";
import { signup } from "../services/userServices.js";
import { useNavigate } from "react-router-dom";

export const SignUpForm = () => {

    // declaración de estados
    
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    


    // hooks de react router para redireccionar
    const navigate = useNavigate()

    // función info del login
    async function handleSubmit(e) {
        e.preventDefault()

        let signupSucceed = await signup(email, password);
        console.log(signupSucceed);

        if (signupSucceed) {
            navigate("/login")
        }

    }

    
    return (
        <form role="form" className="w-50 mx-auto text-start" onSubmit={handleSubmit}>
            <div className="form-group">
            
                <label htmlFor="email" className="form-label ms-1 mb-0">Email<strong style={{ color: "red" }}>*</strong></label>
                <input className="form-control mb-3" id="email" maxLength="120" name="email" required type="text" placeholder="name@example.com" value={email} onChange={(e) => setEmail(e.target.value)} />

                <label htmlFor="password" className="form-label ms-1 mb-0">Contraseña<strong style={{ color: "red" }}>*</strong></label>
                <input className="form-control mb-3" id="password" name="password" required type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

            </div>
            <hr />
            <div className="form-group text-center">
                <div className="submit-row">
                    <input type="submit" className="btn btn-primary mx-2" value="Enviar" />
                    <a href="/" className="btn btn-danger mx-2" role="button">Cancelar</a>
                </div>
            </div>
        </form>
    )
}; 