import { Autocomplete, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { Controller, useFormContext } from 'react-hook-form';
import { useAxios } from '../../../hooks/useAxios';
import { Ingredient } from '../../../types/Ingredient';
import { Unit } from '../../../types/Unit';

const AutoCompleteUnit = () => {
  const name = 'unitId';
  const label = 'Scale';
  const { control, setValue, watch } = useFormContext();
  const { api } = useAxios();
  const [options, setOptions] = useState<readonly Unit[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [optionValue, setOptionValue] = useState<Unit | null>(null);
  const watchIngredient: Ingredient | null = watch('ingredient', null);

  // Prefetch all the available units at the beginning
  useEffect(() => {
    (async () => {
      setIsLoading(true);
      const res = await api.get(`/units`);
      setIsLoading(false);
      setOptions(res.data);
    })();
  }, []);

  // Update the unit options tailored for the selected ingredient
  useEffect(() => {
    (async () => {
      if (!watchIngredient) {
        return;
      }
      setIsLoading(true);
      const res = await api.get(`/units?ingredient_id=${watchIngredient.id}`);
      setIsLoading(false);
      setOptions(res.data);
    })();
  }, [watchIngredient]);

  return (
    <Controller
      control={control}
      name={name}
      defaultValue=""
      render={() => (
        <Autocomplete
          options={options}
          isOptionEqualToValue={(option, value) => option.unit === value.unit}
          getOptionLabel={(option) => option.unit || ''}
          loading={isLoading}
          value={optionValue}
          onChange={(_, newValue) => {
            setOptionValue(newValue);
            if (newValue) {
              setValue(name, newValue.id);
            }
          }}
          renderInput={(params) => (
            <TextField {...params} required label={label} />
          )}
        />
      )}
    />
  );
};

export default AutoCompleteUnit;
