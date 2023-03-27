import { Grid, Stack, Typography } from '@mui/material';
import type { FC } from 'react';
import LocalFireDepartmentOutlinedIcon from '@mui/icons-material/LocalFireDepartmentOutlined';
import ModelTrainingOutlinedIcon from '@mui/icons-material/ModelTrainingOutlined';
import EggAltOutlinedIcon from '@mui/icons-material/EggAltOutlined';
import OilBarrelOutlinedIcon from '@mui/icons-material/OilBarrelOutlined';
import RestaurantOutlinedIcon from '@mui/icons-material/RestaurantOutlined';
import { Recipe } from '../types/Recipe';
import { Theme } from '@emotion/react';

const NutritionBlockTheme: Theme = {
  padding: 1,
  boxShadow: 'inset 0 -7px 9px -7px rgba(0,0,0,0.4)',
  display: 'flex',
  alignItems: 'center',
  flexWrap: 'wrap',
};

const NutritionBlockGray: Theme = {
  backgroundColor: 'grey.100',
  ...NutritionBlockTheme,
};

const NutritionBlockInfo: Theme = {
  backgroundColor: 'primary.dark',
  color: 'white',
  ...NutritionBlockTheme,
};

const NutritionBlockWarning: Theme = {
  backgroundColor: 'info.dark',
  color: 'white',
  ...NutritionBlockTheme,
};

export const RecipeItemNutrition: FC<{ recipe: Recipe }> = ({ recipe }) => {
  return (
    <Grid container className="recipe-nutrition-block">
      <Grid item xs={6} md={3}>
        <Stack direction="row" spacing={1} sx={NutritionBlockInfo}>
          <RestaurantOutlinedIcon sx={{ width: 17 }} />
          <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
            {Math.floor(recipe.numServings)} Servings
          </Typography>
        </Stack>
      </Grid>
      <Grid item xs={6} md={3}>
        <Stack direction="row" spacing={1} sx={NutritionBlockWarning}>
          <LocalFireDepartmentOutlinedIcon sx={{ width: 17 }} />
          <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
            {recipe.nutrition &&
              Math.floor(recipe.nutrition.caloriesKcalPerServing)}{' '}
            kCal
          </Typography>
        </Stack>
      </Grid>
      <Grid item xs={6} sm={4} md={2}>
        <Stack direction="row" spacing={1} sx={NutritionBlockGray}>
          <ModelTrainingOutlinedIcon sx={{ width: 17 }} />
          <Typography variant="body1">
            Carb:{' '}
            {recipe.nutrition &&
              Math.floor(recipe.nutrition.carbsGramPerServing)}
            g
          </Typography>
        </Stack>
      </Grid>
      <Grid item xs={6} sm={4} md={2}>
        <Stack direction="row" spacing={1} sx={NutritionBlockGray}>
          <OilBarrelOutlinedIcon sx={{ width: 17 }} />
          <Typography variant="body1">
            Fat:{' '}
            {recipe.nutrition && Math.floor(recipe.nutrition.fatGramPerServing)}
            g
          </Typography>
        </Stack>
      </Grid>
      <Grid item xs={12} sm={4} md={2}>
        <Stack direction="row" spacing={1} sx={NutritionBlockGray}>
          <EggAltOutlinedIcon sx={{ width: 17 }} />
          <Typography variant="body1">
            Protein:{' '}
            {recipe.nutrition &&
              Math.floor(recipe.nutrition.proteinGramPerServing)}
            g
          </Typography>
        </Stack>
      </Grid>
    </Grid>
  );
};
