export const Private = () => {

    let greeting = "Estás intentando entrar en una página privada. Por favor, inicia sesión o regístrate para entrar y verla."

    if (localStorage.getItem("user_logged") != null) {
        greeting = "Bienvenide a la página privada de " + localStorage.getItem("user_logged")
    }

    return (
        <div className="text-center mt-5">
            <h1 className="w-50 mx-auto">{greeting}</h1>
        </div>
    );
}; 