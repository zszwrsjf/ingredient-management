import React, { Fragment, useContext, useState } from 'react';
import {
  Box,
  Button,
  SnackbarCloseReason,
  TextField,
  Typography,
} from '@mui/material';
import { Stack } from '@mui/system';
import { FormProvider, useForm } from 'react-hook-form';
import AuthContext from '../../../context/authContext';
import { useNavigate } from 'react-router-dom';
import { AxiosError } from 'axios';
import CustomSnackbar from '../../CustomSnackbar';
import { Link } from 'react-router-dom';
import { useAxios } from '../../../hooks/useAxios';
import { Token } from '../../../types/Token';
import { TAuthContext } from '../../../types/AuthContext';
import InputPassword from '../InputPassword';
import LoadingOverlay from '../../LoadingOverlay';

type FormValues = {
  username: string;
  password: string;
};

const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const methods = useForm<FormValues>();
  const authCtx = useContext(AuthContext) as TAuthContext;
  const { api, refreshIntercept } = useAxios();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState({ message: '', isError: false });

  const handleLogin = async (data: FormValues) => {
    setIsLoading(true);
    try {
      api.interceptors.response.eject(refreshIntercept);
      const res = await api.post('/token', data);
      authCtx.postLogin(res.data as Token);
      setIsLoading(false);
      methods.reset({ username: '', password: '' });
      navigate('/ingredients', { replace: true });
    } catch (err) {
      console.log(err);
      if (err instanceof AxiosError) {
        setError({
          message: err.response?.data?.detail || err.message,
          isError: true,
        });
      } else {
        setError({
          message: 'Unknown error',
          isError: true,
        });
      }
      setIsLoading(false);
    }
  };

  const submitHandler = (event: React.FormEvent) => {
    event.preventDefault();
    methods.handleSubmit(handleLogin)();
  };

  const handleCloseSnack = (
    _event: Event | React.SyntheticEvent<any, Event>,
    reason: SnackbarCloseReason
  ) => {
    if (reason === 'clickaway') {
      return;
    }
    setError((prevError) => {
      return { ...prevError, isError: false };
    });
  };

  return (
    <Fragment>
      <LoadingOverlay isLoading={isLoading} />
      <FormProvider {...methods}>
        <Stack component="form" onSubmit={submitHandler} spacing={3}>
          <TextField
            label="Username"
            required
            {...methods.register('username', {
              required: 'This field is required',
            })}
            error={!!methods.formState.errors.username}
            helperText={methods.formState.errors.username?.message}
          />
          <InputPassword name="password" label="Password" required />
          <Button type="submit" variant="contained" color="secondary">
            Log in
          </Button>
          <Typography textAlign="center">
            New to this app?
            <Box component="span" sx={{ marginLeft: '2px' }}>
              <Link to="/auth/signup">Create an account</Link>
            </Box>
          </Typography>
        </Stack>
        <CustomSnackbar
          severity="error"
          message={error.message}
          open={error.isError}
          handleClose={handleCloseSnack}
          showDuration={4000}
        />
      </FormProvider>
    </Fragment>
  );
};

export default LoginForm;
