import { getUser } from '@/lib/api/requests';
import { createContext, useContext, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';

export const INITIAL_USER = {
    _id: "",
    email: "",
    username: "",
    full_name: "",
    bio: "",
    profile_picture_url: ""
};
const INITIAL_STATE = {
  user: INITIAL_USER,
  isLoading: false,
  isAuthenticated: false,
  setUser: () => {},
  setIsAuthenticated: () => {},
  checkAuthUser: async () => false,
};

const AuthContext = createContext(INITIAL_STATE)

export function AuthProvider({ children }) {
    const navigate = useNavigate()
    const [user, setUser] = useState(INITIAL_USER);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const checkAuthUser = async () => {
        setIsLoading(true)
        try {
            const response = await getUser()
            if (response)
                setUser(response)
                setIsAuthenticated(true)
                return true
        }
        catch (error) {
            console.error(`Authentication failed : ${error}`)
            return false
        }
        finally {
            setIsLoading(false)
        }
    }
    useEffect(() => {
        const tokenObject = localStorage.getItem('Token');
        
        if (tokenObject === "[]" || tokenObject === null || tokenObject === undefined) {
            navigate("/sign-in");
        }
        
        
        checkAuthUser();
    }, []);

    const value = {
        user,
        setUser,
        isAuthenticated,
        isLoading,
        checkAuthUser
    }
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}

export const useUserContext = () => useContext(AuthContext)