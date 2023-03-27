import { Button, Stack } from '@mui/material';
import { memo, useState } from 'react';
import { Ingredient } from '../../../types/Ingredient';
import ManualForm from './ManualForm';

type Props = {
  onSubmit: (ingredient: Ingredient) => void;
  manualOnly?: boolean;
};

const IngredientForm = memo(function _(props: Props) {
  const [manual, setManual] = useState(true);

  const manualForm = <ManualForm onSubmit={props.onSubmit} />;

  if (props.manualOnly) {
    return manualForm;
  }

  return (
    <Stack spacing={3}>
      <Stack direction="row">
        <Button
          variant="contained"
          onClick={() => setManual(true)}
          fullWidth={true}
          color={manual ? 'primary' : 'inherit'}
          sx={{
            borderTopRightRadius: 0,
            borderBottomLeftRadius: 0,
            borderBottomRightRadius: 0,
          }}
        >
          INPUT MANUALLY
        </Button>
        <Button
          variant="contained"
          onClick={() => setManual(false)}
          fullWidth={true}
          color={!manual ? 'primary' : 'inherit'}
          sx={{
            borderTopLeftRadius: 0,
            borderBottomLeftRadius: 0,
            borderBottomRightRadius: 0,
          }}
        >
          UPLOAD RECEIPT
        </Button>
      </Stack>
      {manual && manualForm}
    </Stack>
  );
});

export default IngredientForm;
