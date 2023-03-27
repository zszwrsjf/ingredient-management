import { Backdrop, CircularProgress } from '@mui/material';
import * as React from 'react';

type LoadingOverlayProps = {
  isLoading: boolean;
};

const LoadingOverlay: React.FunctionComponent<LoadingOverlayProps> = (
  props
) => {
  return (
    <Backdrop
      sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
      open={props.isLoading}
    >
      <CircularProgress color="inherit" />
    </Backdrop>
  );
};

export default LoadingOverlay;
