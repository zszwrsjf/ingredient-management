import { SxProps } from '@mui/material';

export type FormInput<T> = {
  name: string;
  default: T;
  label?: string;
  required?: boolean;
  sx?: SxProps;
};
