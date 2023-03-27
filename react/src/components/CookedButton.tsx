import * as React from 'react';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import { Box, Button } from '@mui/material';

type CookedButtonProps = {
  filled: boolean | unknown;
  size: 'small' | 'medium' | 'large';
  onClick: (event: React.MouseEvent<HTMLElement>) => void;
};

const CookedButton: React.FunctionComponent<CookedButtonProps> = (props) => {
  return (
    <Button
      variant="contained"
      color={props.filled ? 'highlight' : 'inactive'}
      size="small"
      onClick={props.onClick}
      endIcon={<CheckBoxIcon />}
      disableElevation
      sx={{ marginRight: 1 }}
      fullWidth
    >
      <Box>cooked</Box>
    </Button>
  );
};

export default CookedButton;
