import { Visibility, VisibilityOff } from '@mui/icons-material';
import {
  FormControl,
  FormHelperText,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
} from '@mui/material';
import { useState } from 'react';
import { Controller, useFormContext } from 'react-hook-form';
import { FormInput } from '../../types/Form';

type Props = Omit<FormInput<string>, 'default'> & {
  default?: string;
};

const InputPassword = (props: Props) => {
  const [showPassword, setShowPassword] = useState(false);
  const { control, formState } = useFormContext();

  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const handleMouseDownPassword = (
    event: React.MouseEvent<HTMLButtonElement>
  ) => {
    event.preventDefault();
  };

  return (
    <Controller
      control={control}
      name={props.name}
      defaultValue={props.default || ''}
      rules={{
        required: 'This field is required',
      }}
      render={({ field }) => (
        <FormControl variant="outlined" error={!!formState.errors[props.name]}>
          <InputLabel htmlFor="outlined-adornment-password">
            Password
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            type={showPassword ? 'text' : 'password'}
            value={field.value}
            onChange={field.onChange}
            endAdornment={
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label={props.label || 'Password'}
          />
          <FormHelperText>
            {formState.errors[props.name]?.message as string | undefined}
          </FormHelperText>
        </FormControl>
      )}
    />
  );
};
export default InputPassword;
