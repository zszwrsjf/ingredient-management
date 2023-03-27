import { Controller, useFormContext } from 'react-hook-form';
import { Dayjs } from 'dayjs';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { TextField } from '@mui/material';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { FormInput } from '../../types/Form';

type Props = FormInput<Dayjs> & {
  format?: string;
};

const InputDate = (props: Props) => {
  const { control } = useFormContext();

  return (
    <Controller
      control={control}
      name={props.name}
      defaultValue={props.default}
      render={({ field }) => (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DatePicker
            label={props.label}
            inputFormat={props.format}
            value={field.value}
            onChange={field.onChange}
            renderInput={(params) => <TextField {...params} sx={props.sx} />}
          />
        </LocalizationProvider>
      )}
    />
  );
};

export default InputDate;
