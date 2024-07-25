import apiClient from "./axios";


export async function getUser() {
	try {
		const response = await apiClient.get('/auth/me');

		return response.data;
	} catch (error) {
		console.error(`Error in 'getUser': ${error}`);
		throw error; // Throw the error so it can be caught in checkAuthUser
	}
}

export async function createUserAccount(newUser) {   
    try {
        const response = await apiClient.post('auth/register', JSON.stringify(newUser))
        const tokenObject = response.data
        if (!tokenObject)
            throw new Error()
        localStorage.setItem('Token', JSON.stringify(tokenObject)) 
    }
    catch (error) {
        console.error(`Error in 'createUserAccount': ${error}`);
		throw error;
    }  
}

export async function signInAccount(userCredential) {
    try {
        const response = await apiClient.post('auth/login',
            new URLSearchParams({   // 2. Use URLSearchParams to encode the data
                username: userCredential.email,  // 3. Add the username (or email) and password to the body
                password: userCredential.password
            }),
            {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'  // 1. Set the Content-Type header to application/x-www-form-urlencoded
            }}
        )
        const tokenObject = response.data
        if (!tokenObject)
            throw new Error()
        localStorage.setItem('Token', JSON.stringify(tokenObject))
    }
    catch (error) {
        console.error(`Error signInAccount : ${error}`)
        throw new Error()
    }
}

export async function signOut() {
    try {
        const response = await apiClient.post('auth/logout')

        if (response.status !== 200)
            throw new Error()
        localStorage.removeItem('Token')
    }
    catch (error) {
        console.error(`SignOut Failed ${error}`)
        throw new Error()
    }
}