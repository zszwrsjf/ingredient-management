import {
  Box,
  Container,
  CssBaseline,
  Divider,
  Paper,
  Typography,
} from '@mui/material';
import { Stack } from '@mui/system';
import { FC, Fragment, PropsWithChildren } from 'react';
import theme from '../../themes/theme';
import MyAppBar from './MyAppBar';

const Layout: FC<PropsWithChildren> = ({ children }) => {
  return (
    <Fragment>
      <CssBaseline />
      <Box
        sx={{
          display: 'grid',
          gridTemplateRows: 'auto 1fr auto',
          minHeight: '100vh',
        }}
      >
        <MyAppBar />
        <Container sx={{ flex: 'none', paddingY: 5 }}>{children}</Container>
        <Paper
          sx={{
            width: '100%',
            backgroundColor: theme.palette.primary.dark,
            color: 'white',
            marginTop: 2,
          }}
          square
        >
          <Container sx={{ padding: 2 }}>
            <Stack direction="row" spacing={1}>
              <Typography variant="body1" sx={{ fontWeight: 900 }}>
                Health Up
              </Typography>
              <Typography variant="body1">(2022)</Typography>
              <Typography variant="body1" sx={{ pl: 3 }}>
                Manage your fridge, eat healthier and enjoy cooking.
              </Typography>
            </Stack>
          </Container>
        </Paper>
      </Box>
    </Fragment>
  );
};

export default Layout;
