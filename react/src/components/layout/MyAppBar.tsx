import {
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Button,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import * as React from 'react';
import PagesMenu from './PagesMenu';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../../context/authContext';
import { TAuthContext } from '../../types/AuthContext';
import LogoutIcon from '@mui/icons-material/Logout';
import LoginIcon from '@mui/icons-material/Login';
import { useState } from 'react';
import theme from '../../themes/theme';

const MyAppBar: React.FunctionComponent = () => {
  const authCtx = React.useContext(AuthContext) as TAuthContext;

  const navigate = useNavigate();

  const [pagesAnchorEl, setPagesAnchorEl] = useState<HTMLElement | null>(null);
  const pagesHandleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setPagesAnchorEl(event.currentTarget);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            sx={{ mr: 2, display: { xs: 'flex', md: 'none' } }}
            onClick={pagesHandleClick}
          >
            <MenuIcon />
          </IconButton>
          <PagesMenu
            anchorEl={pagesAnchorEl}
            onClose={() => setPagesAnchorEl(null)}
          />
          <Button
            variant="text"
            component="h6"
            sx={{
              mr: 2,
              color: theme.palette.grey[900],
              fontSize: 20,
              fontWeight: 'bold',
            }}
            onClick={() => navigate('/')}
          >
            Health Up
          </Button>
          <Box
            sx={{
              display: { xs: 'none', md: 'flex' },
            }}
          >
            <Button
              color="inherit"
              disableElevation
              onClick={() => navigate('/ingredients')}
            >
              My Ingredients
            </Button>
            <Button
              color="inherit"
              disableElevation
              onClick={() => navigate('/user')}
            >
              User Dashboard
            </Button>
            <Button
              color="inherit"
              disableElevation
              onClick={() => navigate('/recipes')}
              href="/recipes"
            >
              Recipe Search
            </Button>
          </Box>
          <Box flexGrow={1} />
          {authCtx.isLoggedIn ? (
            <Button
              size="large"
              aria-label="logout"
              color="inherit"
              onClick={authCtx.logout}
              endIcon={<LogoutIcon />}
            >
              logout
            </Button>
          ) : (
            <Button
              size="large"
              aria-label="login"
              color="inherit"
              onClick={() => navigate('/auth/login', { replace: true })}
              endIcon={<LoginIcon />}
            >
              login
            </Button>
          )}
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default MyAppBar;
