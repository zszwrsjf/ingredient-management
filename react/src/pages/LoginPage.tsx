import { Box, Container, Typography } from '@mui/material';
import * as React from 'react';
import LoginForm from '../components/form/auth/LoginForm';

const LoginPage: React.FunctionComponent = () => {
  return (
    <Box className="login-page-container">
      <Typography variant="h4" textAlign="center">
        Login
      </Typography>
      <Container maxWidth="xs" sx={{ pt: 5 }}>
        <LoginForm />
      </Container>
    </Box>
  );
};

export default LoginPage;
