import * as React from 'react';
import { Stack } from '@mui/material';
import { Recipe } from '../types/Recipe';
import { RecipeItem } from './RecipeItem';

type RecipeItemListProps = {
  recipes: Recipe[];
  displayNutrition: boolean;
  displayTags: boolean;
};

const RecipeItemList = React.memo(function _(props: RecipeItemListProps) {
  return (
    <Stack className="recipe-list" direction="column" spacing={4}>
      {props.recipes.map((recipe: Recipe) => {
        return (
          <RecipeItem
            key={recipe.id}
            recipe={recipe}
            displayNutrition={props.displayNutrition}
            displayTags={props.displayTags}
          />
        );
      })}
    </Stack>
  );
});

export default RecipeItemList;
