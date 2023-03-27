import { Box, Container, Typography } from '@mui/material';
import * as React from 'react';
import SignupForm from '../components/form/auth/SignupForm';

const SignupPage: React.FunctionComponent = () => {
  return (
    <Box className="login-page-container">
      <Typography variant="h4" textAlign="center">
        Signup
      </Typography>
      <Container maxWidth="xs" sx={{ pt: 5 }}>
        <SignupForm />
      </Container>
    </Box>
  );
};

export default SignupPage;
