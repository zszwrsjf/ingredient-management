import React, { Fragment, useState } from 'react';
import {
  Box,
  Button,
  SnackbarCloseReason,
  TextField,
  Typography,
} from '@mui/material';
import { Stack } from '@mui/system';
import { FormProvider, useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { AxiosError } from 'axios';
import CustomSnackbar from '../../CustomSnackbar';
import { Link } from 'react-router-dom';
import { useAxios } from '../../../hooks/useAxios';
import InputPassword from '../InputPassword';
import LoadingOverlay from '../../LoadingOverlay';
import { emailRegEx } from '../../../util/misc';

type FormValues = {
  username: string;
  email: string;
  password: string;
};

const SignupForm: React.FC = () => {
  const navigate = useNavigate();
  const methods = useForm<FormValues>();
  const { api, refreshIntercept } = useAxios();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState({ message: '', isError: false });

  const handleSignup = async (data: FormValues) => {
    setIsLoading(true);
    try {
      api.interceptors.response.eject(refreshIntercept);
      await api.post('/signup', data);
      methods.reset({ username: '', email: '', password: '' });
      navigate('/auth/login');
    } catch (err) {
      console.log(err);
      if (err instanceof AxiosError) {
        let message = err.message;
        if (err.response?.data?.username) {
          message = err.response?.data?.username[0];
        } else if (err.response?.data?.email) {
          message = err.response?.data?.email[0];
        }
        setError({ message: message, isError: true });
      } else {
        setError({ message: 'Unknown error', isError: true });
      }
    }
    setIsLoading(false);
  };

  const submitHandler = (event: React.FormEvent) => {
    event.preventDefault();
    methods.handleSubmit(handleSignup)();
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
          <TextField
            label="Email"
            required
            type="email"
            {...methods.register('email', {
              required: 'This field is required',
              pattern: { value: emailRegEx, message: 'Invalid email' },
            })}
            error={!!methods.formState.errors.email}
            helperText={methods.formState.errors.email?.message}
          />
          <InputPassword name="password" label="Password" required />
          <Button type="submit" variant="contained" color="secondary">
            Sign up
          </Button>
          <Typography textAlign="center">
            Already have an account?
            <Box component="span" sx={{ marginLeft: '2px' }}>
              <Link to="/auth/login">Sign in</Link>
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

export default SignupForm;
