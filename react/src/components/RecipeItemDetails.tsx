import type { FC, PropsWithChildren } from 'react';
import styled from '@emotion/styled';
import { Recipe } from '../types/Recipe';
import { Box, Typography, Button, Grid } from '@mui/material';
import { Stack } from '@mui/system';
import { Ingredient } from '../types/Ingredient';
import { Theme } from '@emotion/react';
import theme from '../themes/theme';
import { RecipeIngredient } from '../types/RecipeIngredient';

const RecipeImage = styled('img')`
  flex-shrink: 0;
  width: 100%;
  max-height: 250px;
  object-fit: cover;
  border-radius: 5%;
  background-position: center center;
  background-repeat: no-repeat;
`;

const IngredientIndicationTheme: Theme = {
  fillOpacity: 0.5,
  paddingY: 0.5,
  paddingX: 1,
  border: 2,
  borderRadius: 2,
  textTransform: 'capitalize',
};
const IngredientIndicationPositive: Theme = {
  color: 'success.main',
  ...IngredientIndicationTheme,
};
const IngredientIndicationNegative: Theme = {
  color: 'error.main',
  ...IngredientIndicationTheme,
};

export const RecipeItemDetails: FC<PropsWithChildren<{ recipe: Recipe }>> = ({
  recipe,
  children,
}) => {
  return (
    <Box className="recipe-item-details" padding={2}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Box
            className="recipe-item-image img"
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              overflow: 'hidden',
            }}
          >
            <RecipeImage
              src={recipe.imageUrl}
              alt={recipe.title}
              loading={'lazy'}
            />
          </Box>
        </Grid>
        <Grid item xs={12} md={9}>
          <Stack direction="column" spacing={1}>
            <Typography variant="h4" sx={{ textTransform: 'capitalize' }}>
              {recipe.title}
            </Typography>
            <Box className="recipe-item-ingredients">
              <Stack
                direction="row"
                spacing={0}
                sx={{ flexWrap: 'wrap', columnGap: 2, rowGap: 1 }}
              >
                {recipe.ingredients?.map((ri: RecipeIngredient) => {
                  return (
                    <Box
                      key={ri.id}
                      className="recipe-ingredient"
                      sx={
                        ri.ingredient.inStorage
                          ? IngredientIndicationPositive
                          : IngredientIndicationNegative
                      }
                    >
                      <Typography variant="body1" sx={{ fontWeight: 900 }}>
                        {ri.ingredient.name}
                      </Typography>
                    </Box>
                  );
                })}
                {recipe.ingredients &&
                  recipe.ingredients.length !== recipe.numIngredients && (
                    <Typography
                      variant="body2"
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        flexWrap: 'wrap',
                      }}
                    >
                      (and {recipe.numIngredients - recipe.ingredients.length}{' '}
                      more)
                    </Typography>
                  )}
              </Stack>
            </Box>
            <Box paddingY={1}>{children}</Box>
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};
