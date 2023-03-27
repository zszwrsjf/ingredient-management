import { Input, Slider, Stack } from '@mui/material';
import { Controller, useFormContext } from 'react-hook-form';
import { FormInput } from '../../types/Form';

type Props = FormInput<number> & {
  min?: number;
  max?: number;
  step?: number;
};

const InputSliderWithNum = (props: Props) => {
  const { control } = useFormContext();

  return (
    <Controller
      control={control}
      name={props.name}
      defaultValue={props.default}
      rules={{ required: props.required, min: props.min, max: props.max }}
      render={({ field }) => (
        <Stack direction="row" spacing={2} alignItems="center" sx={props.sx}>
          <Slider
            value={Number(field.value)}
            onChange={field.onChange}
            valueLabelDisplay="auto"
            min={props.min}
            max={props.max}
            step={props.step}
          />
          <Input
            value={Number(field.value)}
            size="small"
            onChange={field.onChange}
            onBlur={field.onBlur}
            inputProps={{
              min: props.min,
              max: props.max,
              step: props.step,
              type: 'number',
            }}
          />
        </Stack>
      )}
    />
  );
};

export default InputSliderWithNum;
