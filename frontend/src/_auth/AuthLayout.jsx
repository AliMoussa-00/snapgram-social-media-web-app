import { Navigate, Outlet } from 'react-router-dom';
import { useUserContext } from '@/context/AuthContext';

const AuthLayout = () => {
  const { isAuthenticated } = useUserContext();
  
  return (
    <>
      {isAuthenticated ? (
        <Navigate to='/'/>
      ) : (
          <>
            <section className='flex flex-1 flex-col justify-center items-center py-10'>
              <Outlet/>
            </section>

            <img
              src='/assets/images/side-img.svg'
              alt='side-image'
              className='hidden xl:block h-screen w-1/2 object-cover bg-no-repeat'
            />
          </>
      )}
    </>
  )
}

export default AuthLayout