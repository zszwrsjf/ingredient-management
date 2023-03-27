import { Button } from '@mui/material';
import * as React from 'react';
import KeyboardArrowRightOutlinedIcon from '@mui/icons-material/KeyboardArrowRightOutlined';

interface IViewRecipeButtonProps {
  size: 'small' | 'medium' | 'large';
  href: string;
  onClick: (event: React.MouseEvent<HTMLElement>) => void;
}

const ViewRecipeButton: React.FunctionComponent<IViewRecipeButtonProps> = (
  props
) => {
  return (
    <Button
      target="_blank"
      href={props.href}
      onClick={props.onClick}
      variant="contained"
      size="small"
      color="secondary"
      endIcon={<KeyboardArrowRightOutlinedIcon />}
      disableElevation
      fullWidth
    >
      view
    </Button>
  );
};

export default ViewRecipeButton;
