import { styled } from '@mui/material/styles';
import LinearProgress, {
  linearProgressClasses,
} from '@mui/material/LinearProgress';

export const ShelfLifeDaysBar = styled(LinearProgress)<{ dayleft: number }>(
  ({ value, dayleft, theme }) => ({
    height: 10,
    borderRadius: 5,
    [`&.${linearProgressClasses.colorPrimary}`]: {
      backgroundColor: theme.palette.grey[200],
    },
    [`& .${linearProgressClasses.bar}`]: {
      borderRadius: 5,
      backgroundColor: (() => {
        if (typeof value === 'undefined') {
          return theme.palette.grey[200];
        } else if (dayleft <= 1) {
          return theme.palette.error.main;
        } else if (dayleft <= 5) {
          return theme.palette.warning.main;
        } else {
          return theme.palette.primary.main;
        }
      })(),
    },
  })
);
