import {
  Divider,
  Link,
  ListItemIcon,
  ListItemText,
  Menu,
  MenuItem,
  Typography,
} from '@mui/material';
import * as React from 'react';
import KitchenIcon from '@mui/icons-material/Kitchen';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ManageSearchIcon from '@mui/icons-material/ManageSearch';
import { useNavigate } from 'react-router-dom';

type PagesMenuProps = {
  anchorEl: HTMLElement | null;
  onClose: () => void;
};

const PagesMenu: React.FunctionComponent<PagesMenuProps> = (props) => {
  const navigate = useNavigate();
  const sentTo = (to: string) => {
    props.onClose();
    navigate(to);
  };
  return (
    <Menu
      id="page-menu"
      anchorEl={props.anchorEl}
      open={Boolean(props.anchorEl)}
      onClose={props.onClose}
    >
      <MenuItem onClick={() => sentTo('/ingredients')}>
        <KitchenIcon fontSize="small" sx={{ mr: 1 }} />
        <Typography variant="body1">My Ingredients</Typography>
      </MenuItem>
      <MenuItem onClick={() => sentTo('/user')}>
        <AccountCircleIcon fontSize="small" sx={{ mr: 1 }} />
        <Typography variant="body1">User Dashboard</Typography>
      </MenuItem>
      <Divider />
      <MenuItem onClick={() => sentTo('/recipes')} href="/recipes">
        <ManageSearchIcon fontSize="small" sx={{ mr: 1 }} />
        <Typography variant="body1">Recipe Search</Typography>
      </MenuItem>
    </Menu>
  );
};

export default PagesMenu;
