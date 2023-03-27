import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import { Controller, useFormContext } from 'react-hook-form';
import { FormInput } from '../../types/Form';

type Props<T> = FormInput<T> & {
  items: Array<T>;
};

const InputSelect = <T,>(props: Props<T>) => {
  const { control } = useFormContext();

  return (
    <Controller
      control={control}
      name={props.name}
      defaultValue={props.default}
      render={({ field }) => (
        <FormControl sx={props.sx}>
          <InputLabel>{props.label}</InputLabel>
          <Select
            label={props.label}
            defaultValue={props.default}
            value={field.value}
            onChange={field.onChange}
          >
            {props.items.map((i) => (
              <MenuItem value={i as string} key={i as string}>
                {i as string}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )}
    />
  );
};

export default InputSelect;
