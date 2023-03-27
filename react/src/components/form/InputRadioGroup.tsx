import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Tooltip,
} from '@mui/material';
import { Controller, useFormContext } from 'react-hook-form';
import { FormInput } from '../../types/Form';

type Props<T> = FormInput<T> & {
  options: Array<T>;
  datatip?: string[];
  row?: boolean;
};

export const InputRadioGroup = <T,>(props: Props<T>) => {
  const { control } = useFormContext();

  return (
    <Controller
      control={control}
      name={props.name}
      defaultValue={props.default}
      render={({ field }) => (
        <FormControl>
          {props.label && <FormLabel>{props.label}</FormLabel>}
          <RadioGroup
            value={field.value}
            onChange={field.onChange}
            row={props.row}
          >
            {props.options.map((i, index) => {
              const formContextLabel = (
                <FormControlLabel
                  key={i as string}
                  value={i as string}
                  control={<Radio />}
                  label={(i as string).toUpperCase()}
                />
              );
              if (!props.datatip) {
                return formContextLabel;
              } else {
                return (
                  <Tooltip
                    title={props.datatip[index]}
                    key={i as string}
                  >
                    {formContextLabel}
                  </Tooltip>
                );
              }
            })}
          </RadioGroup>
        </FormControl>
      )}
    />
  );
};
