import FavoriteIcon from '@mui/icons-material/Favorite';
import { Box, Button, Stack, TextField } from '@mui/material';
import { useCallback, useEffect } from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import { Ingredient } from '../../../types/Ingredient';
import dayjs, { Dayjs } from 'dayjs';
import InputDate from '../InputDate';
import InputSliderWithNum from '../InputSliderWithNum';
import AutoCompleteIngredient from './AutoCompleteIngredient';
import AutoCompleteUnit from './AutoCompleteUnit';
import { useAxios } from '../../../hooks/useAxios';
import { InputRadioGroup } from '../InputRadioGroup';

type Props = {
  onSubmit: (ingredient: Ingredient) => void;
};

type Inputs = {
  ingredient: Ingredient;
  quantity: number;
  unitId: number;
  storage: 'Pantry' | 'Fridge' | 'Freezer';
  expiration: Dayjs;
  happiness: number;
};

const storageStrToInt = (storage: 'Pantry' | 'Fridge' | 'Freezer') => {
  switch (storage) {
    case 'Pantry':
      return 0;
    case 'Fridge':
      return 1;
    default:
      return 2;
  }
};

const ManualForm = ({ onSubmit }: Props) => {
  const methods = useForm<Inputs>();
  const { api } = useAxios();
  const watchStorage = methods.watch('storage');
  const watchIngredient: Ingredient | null = methods.watch('ingredient');

  /// send POST req to the API
  const postIngredient = useCallback(async (data: Inputs) => {
    const body = {
      quantity_scale_unit_id: data.unitId,
      ingredient_id: data.ingredient.id,
      expiration_date: data.expiration.toISOString(),
      happiness: data.happiness,
      storage: storageStrToInt(data.storage),
      quantity_value: data.quantity,
    };
    try {
      const res = await api.post('/user/ingredients', body);
      if (onSubmit) onSubmit(res.data);
    } catch (err) {
      console.log(err);
    }
  }, []);

  const submitHandler = useCallback((event: React.FormEvent) => {
    event.preventDefault(); // prevent page refresh
    methods.handleSubmit(postIngredient)();
  }, []);

  const onIngredientSelect = useCallback((i: Ingredient) => {
    setStorageOnIngredientSelect(i);
  }, []);

  // set the default storage option
  const setStorageOnIngredientSelect = useCallback((i: Ingredient) => {
    const _storage = i.refrigeratorDays
      ? 'Fridge'
      : i.freezerDays
      ? 'Freezer'
      : 'Pantry';
    methods.setValue('storage', _storage);
  }, []);

  // update the default expiration date upon 'Storage' selection
  useEffect(() => {
    if (!watchIngredient) {
      return;
    }
    let diff = 0;
    switch (watchStorage) {
      case 'Pantry':
        diff = watchIngredient.pantryDays || 0;
        break;
      case 'Fridge':
        diff = watchIngredient.refrigeratorDays || 0;
        break;
      case 'Freezer':
        diff = watchIngredient.freezerDays || 0;
        break;
    }
    methods.setValue('expiration', dayjs().startOf('d').add(diff, 'd'));
  }, [watchStorage, watchIngredient, methods.setValue]);

  return (
    <FormProvider {...methods}>
      <Stack component="form" onSubmit={submitHandler} spacing={3}>
        <AutoCompleteIngredient required onSelect={onIngredientSelect} />

        <Stack direction="row" justifyContent="space-between" spacing={2}>
          <TextField
            required
            label="Quantity"
            inputProps={{
              step: 0.1,
              type: 'number',
            }}
            {...methods.register('quantity', {
              required: true,
              min: 0,
              valueAsNumber: true,
            })}
            sx={{ flex: '1' }}
          />
          <AutoCompleteUnit />
        </Stack>

        <Box display="flex" justifyContent="center" alignItems="center">
          <InputRadioGroup
            default="Fridge"
            name="storage"
            options={['Pantry', 'Fridge', 'Freezer']}
            row
          />
        </Box>

        <InputDate
          name="expiration"
          default={dayjs().startOf('d')}
          label="Expiration"
          format="MM/DD/YYYY"
        />

        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          spacing={2}
        >
          <FavoriteIcon />
          <InputSliderWithNum
            name="happiness"
            default={80}
            required
            min={0}
            max={100}
            step={5}
            sx={{ flex: '1' }}
          />
        </Stack>

        <Button type="submit" variant="contained" size="large">
          Register
        </Button>
      </Stack>
    </FormProvider>
  );
};

export default ManualForm;
