import { Backdrop, CircularProgress } from '@mui/material';
import { useContext } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import AuthContext from '../context/authContext';
import { TAuthContext } from '../types/AuthContext';

const PrivateRoute = () => {
  const authCtx = useContext(AuthContext) as TAuthContext;

  if (authCtx.isLoggedIn) {
    return <Outlet />;
  } else if (authCtx.isLoading) {
    return (
      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    );
  } else {
    return <Navigate to="/auth/login" replace={true} />;
  }
};

export default PrivateRoute;
