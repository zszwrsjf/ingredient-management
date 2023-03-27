import { Paper } from '@mui/material';
import * as React from 'react';
import { Recipe } from '../types/Recipe';
import { RecipeItemActions } from './RecipeItemActions';
import { RecipeItemDetails } from './RecipeItemDetails';
import { RecipeItemNutrition } from './RecipeItemNutrition';
import { RecipeItemTags } from './RecipeItemTags';

type RecipeItemProps = React.PropsWithChildren<{
  recipe: Recipe;
  displayNutrition?: boolean;
  displayTags?: boolean;
}>;

export const RecipeItem = React.memo(function _(props: RecipeItemProps) {
  return (
    <Paper className="recipe-list-item" elevation={4}>
      {props.displayNutrition && <RecipeItemNutrition recipe={props.recipe} />}
      <RecipeItemDetails recipe={props.recipe}>
        {props.children}
      </RecipeItemDetails>
      <RecipeItemActions recipe={props.recipe} />
      {props.displayTags && <RecipeItemTags recipe={props.recipe} />}
    </Paper>
  );
});

export default RecipeItem;
