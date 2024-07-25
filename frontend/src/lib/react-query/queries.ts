import { useMutation } from "@tanstack/react-query";
import { createUserAccount, signInAccount, signOut } from "../api/requests";


export const useCreateUserAccount = () => {
    return useMutation({
        mutationFn:(newUser) => createUserAccount(newUser)
    })
}

export const useSignInAccount = () => {
    return useMutation({
        mutationFn: (userCredential) => signInAccount(userCredential)
    })
}

export const useSignOut = () => {
    return useMutation({
        mutationFn: () => signOut()
    })
}