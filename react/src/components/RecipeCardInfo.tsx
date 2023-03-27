import { Box, Stack, Chip, Divider, Typography } from '@mui/material';
import * as React from 'react';
import theme from '../themes/theme';
import { Recipe } from '../types/Recipe';
import { floor } from '../util/misc';

type IRecipeCardInfoProps = {
  recipe: Recipe;
};

const RecipeCardInfo: React.FunctionComponent<IRecipeCardInfoProps> = (
  props
) => {
  return (
    <Box sx={{ padding: 1 }}>
      <Chip
        color="secondary"
        variant="outlined"
        size="small"
        label={`${floor(props.recipe.numServings)} Servings`}
      />
      <Divider textAlign="left" sx={{ marginY: 1 }}>
        <Typography variant="body2">Nutrition (per serving)</Typography>
      </Divider>
      <Stack direction="row" sx={{ flexWrap: 'wrap', columnGap: 1, rowGap: 1 }}>
        <Chip
          size="small"
          label={`${floor(
            props.recipe.nutrition?.caloriesKcalPerServing
          )} kCal`}
        />
        <Chip
          size="small"
          label={`${floor(props.recipe.nutrition?.fatGramPerServing)}g Fat`}
        />
        <Chip
          size="small"
          label={`${floor(
            props.recipe.nutrition?.proteinGramPerServing
          )}g Protein`}
        />
        <Chip
          size="small"
          label={`${floor(props.recipe.nutrition?.carbsGramPerServing)}g Carbs`}
        />
      </Stack>
    </Box>
  );
};

export default RecipeCardInfo;
