import * as React from 'react';
import { UserIngredient } from '../types/UserIngredient';
import { IsChecked } from '../types/IsChecked';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import { IngredientCard } from './IngredientCard';
import Checkbox from '@mui/material/Checkbox';
import theme from '../themes/theme';
import CheckIcon from '@mui/icons-material/Check';
import { Typography } from '@mui/material';

type IngredientListProps = {
  userIngredients: UserIngredient[];
  isCheckedState: IsChecked;
  handleChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onAction: () => void;
};

export const IngredientList = React.memo(function _(
  props: IngredientListProps
) {
  const { userIngredients, isCheckedState, handleChange, onAction } = props;

  const [ingredientNum, setIngredientNum] = React.useState(
    userIngredients.length
  );

  React.useEffect(() => {
    setIngredientNum(userIngredients.length);
  }, [JSON.stringify(userIngredients)]);

  const EmptyMessage = () => {
    if (ingredientNum === 0) {
      return (
        <Typography variant="h5">
          There is nothing in your fridge. Click the bottom right button to add
          items.
        </Typography>
      );
    } else {
      return <></>;
    }
  };

  return (
    <Container sx={{ marginTop: 3 }}>
      <>
        <EmptyMessage />
        <Grid container rowSpacing={2} columnSpacing={3}>
          {userIngredients.map((userIngredient) => (
            <Grid item xs={12} md={4} key={userIngredient.id}>
              <IngredientCard
                onAction={onAction}
                userIngredient={userIngredient}
                checkbox={
                  <Checkbox
                    checked={
                      isCheckedState[userIngredient.ingredient.id] || false
                    }
                    onChange={handleChange}
                    name={String(userIngredient.ingredient.id)}
                    size="medium"
                    icon={<CheckIcon />}
                    checkedIcon={<CheckIcon />}
                    sx={{
                      borderRadius: 0,
                      height: '100%',
                      backgroundColor: theme.palette.grey[300],
                      color: theme.palette.grey[600],
                      '&.Mui-checked': {
                        backgroundColor: theme.palette.primary.main,
                        color: theme.palette.grey[50],
                      },
                      '&:hover': {
                        backgroundColor: theme.palette.grey[400],
                      },
                      '&.Mui-checked:hover': {
                        backgroundColor: theme.palette.primary.dark,
                      },
                    }}
                  />
                }
              />
            </Grid>
          ))}
        </Grid>
      </>
    </Container>
  );
});
