import React, { useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Button } from '../ui/button'
import { useSignOut } from '@/lib/react-query/queries'
import { useToast } from '../ui/use-toast'
import { useUserContext } from '@/context/Authcontext'

const Topbar = () => {
    const navigate = useNavigate()
    const toast = useToast()
    const { mutateAsync: signOut, isSuccess } = useSignOut()
    const { user }= useUserContext()

    const onSignOut = async () => {
        try {
            await signOut()            
        }
        catch (error) {
            toast({
                title: 'Sign Out Failed',
                description: 'An unexpected error occurred. Please try again.',
            })
        }
    }
    
    useEffect(() => {
        if (isSuccess)
            navigate(0) // Navigate to refresh the page
    }, [isSuccess])

    return (
        <section className='topbar'>
            <div className='flex-between py-4 px-5'>
                <Link to="/" className="flex gap-3 items-center">
                    <img
                        src='/assets/images/logo.svg'
                        alt='logo'
                        width={130}
                        height={325}
                    />
                </Link>
                <div className='flex gap-4'>
                    <Button variant="ghost" className="shad-button_ghost"
                    onClick={onSignOut}>
                        <img
                            src='/assets/icons/logout.svg'
                            alt='logout'
                        />
                    </Button>
                    <Link to={`/profile/${user._id}}`} className='flex-center gap-3'>
                        <img
                            src={user.profile_picture_url || "/assets/icons/profile-placeholder.svg"}
                            alt="profile"
                            className='h-8 w-8 rounded-full'
                        />
                    </Link>

                </div>

            </div>        
      </section>
  )
}

export default Topbar