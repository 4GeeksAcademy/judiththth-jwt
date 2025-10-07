//sistema de autenticación

export async function login(email, password) {
    try {
        const response = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/login", {
            method: 'POST',
            body: JSON.stringify({ email: email, password: password }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await response.json()
        console.log(data);

        if (response.status === 200) {
            localStorage.setItem('token', data.access_token)
            localStorage.setItem("user_logged", email)
            return true
        }
        if (response.status === 404) {
            return false
        }


    } catch (error) {
        console.log(error)
        return false
    }

}

export async function signup(email, password) {
    try {
        const response = await fetch(import.meta.env.VITE_BACKEND_URL + "/api/signup", {
            method: 'POST',
            body: JSON.stringify({email: email, password: password}),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        const data = await response.json()

        alert(data.msg);
        if (response.ok) {
            return true
        } else {
            return false
        }

    } catch (error) {
        console.log(error)
        return false
    }
}

export async function getUserFavorites() {

    let token = localStorage.getItem("token")
    const myHeaders = new Headers();
    myHeaders.append("Authorization", `Bearer ${token}`)

    const requestOptions = {
        method: "GET",
        headers: myHeaders
    };

    try {
        const response = await fetch(import.meta.env.VITE_BACKEND_URL + "/favorites", requestOptions);
        const result = await response.json();
        console.log(result)
    } catch (error) {
        console.error(error);
    };
}

//validar la autenticación
export async function validAuth() {
    let token = localStorage.getItem("token")
    const myHeaders = new Headers();
    myHeaders.append("Authorization", `Bearer ${token}`)

    const requestOptions = {
        method: "GET",
        headers: myHeaders
    };
    try {
        const response = await fetch(import.meta.env.VITE_BACKEND_URL + "/valid-auth", requestOptions);

        return response.ok
    } catch (error) {
        console.error(error);
    };
}