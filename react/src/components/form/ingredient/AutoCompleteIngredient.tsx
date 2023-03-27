import { Autocomplete, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { Controller, useFormContext } from 'react-hook-form';
import { Ingredient } from '../../../types/Ingredient';
import { useAxios } from '../../../hooks/useAxios';

type Props = {
  onSelect: (_: Ingredient) => void;
  name?: string;
  label?: string;
  required?: boolean;
  timeout?: number;
  noOptionsText?: string;
  clearAfterSelect?: boolean;
};

const AutoCompleteIngredient = (props: Props) => {
  const name = props.name || 'ingredient';
  const label = props.label || 'Ingredient name';
  const timeout = props.timeout || 500;
  const { control, setValue } = useFormContext();
  const { api } = useAxios();
  const [options, setOptions] = useState<readonly Ingredient[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const [optionValue, setOptionValue] = useState<Ingredient | null>(null);

  useEffect(() => {
    const timeoutId = setTimeout(async () => {
      if (!inputValue) {
        setOptions([]);
        return;
      }
      setIsLoading(true);
      const res = await api.get(`/ingredients/search?icontains=${inputValue}`);
      setIsLoading(false);
      setOptions(res.data);
    }, timeout);
    return () => {
      clearTimeout(timeoutId);
    };
  }, [inputValue]);

  const fixShelfLifeDays = (i: Ingredient) => {
    if (!i.freezerDays && !i.refrigeratorDays && !i.pantryDays) {
      i.pantryDays = 2 * 365;
    }
    return i;
  };

  return (
    <Controller
      control={control}
      name={name}
      defaultValue={null}
      render={() => (
        <Autocomplete
          options={options}
          noOptionsText={props.noOptionsText || 'Type something to search'}
          isOptionEqualToValue={(option, value) => option.name === value.name}
          getOptionLabel={(option) => option.name || ''}
          loading={isLoading}
          inputValue={inputValue}
          onInputChange={(_, newInputValue) => {
            setInputValue(newInputValue);
          }}
          value={optionValue}
          onChange={(_, newValue) => {
            setOptionValue(newValue);
            if (newValue) {
              newValue = fixShelfLifeDays(newValue);
              setValue(name, newValue);
              props.onSelect(newValue);
              if (props.clearAfterSelect) {
                setInputValue('');
                setOptionValue(null);
              }
            }
          }}
          filterOptions={(x) => x}
          renderInput={(params) => (
            <TextField {...params} required={props.required} label={label} />
          )}
        />
      )}
    />
  );
};

export default AutoCompleteIngredient;
