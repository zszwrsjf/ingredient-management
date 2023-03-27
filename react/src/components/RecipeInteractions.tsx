import { Box } from '@mui/material';
import * as React from 'react';
import { useAxios } from '../hooks/useAxios';
import { Recipe } from '../types/Recipe';
import CookedButton from './CookedButton';
import FavoriteButton from './FavoriteButton';
import ViewRecipeButton from './ViewRecipeButton';

type RecipeInteractionsProps = {
  recipe: Recipe;
  size: 'small' | 'medium' | 'large';
};

const RecipeInteractions: React.FunctionComponent<RecipeInteractionsProps> = (
  props
) => {
  const { api } = useAxios();
  const [fav, setFav] = React.useState(props.recipe.userFavorite);
  const [cook, setCook] = React.useState(props.recipe.userCooked);
  return (
    <Box
      className="recipe-interactions"
      sx={{ width: '100%', display: 'flex' }}
    >
      <Box sx={{ mr: 1 }}>
        <FavoriteButton
          size={props.size}
          filled={fav}
          onClick={async (event) => {
            event.preventDefault();
            const newVal = !fav;
            try {
              if (newVal) {
                await api.post('/user/favorite', {
                  recipe_id: props.recipe.id,
                });
              } else {
                await api.delete('/user/favorite', {
                  data: {recipe_id: props.recipe.id},
                });
              }
            } catch (err) {
              console.log(err);
            }
            setFav(newVal);
          }}
        />
      </Box>
      <CookedButton
        size={props.size}
        filled={cook}
        onClick={async (event) => {
          event.preventDefault();
          const newVal = !cook;
          try {
            await api.put('/user/recipes', {
              recipe_id: props.recipe.id,
              cooked: newVal,
            });
          } catch (err) {
            console.log(err);
          }
          setCook(newVal);
        }}
      />
      <ViewRecipeButton
        size={props.size}
        href={props.recipe.recipeUrl}
        onClick={async (event) => {
          try {
            await api.post('/user/recipes', {
              recipe_id: props.recipe.id,
            });
          } catch (err) {
            console.log(err);
          }
        }}
      />
    </Box>
  );
};

export default RecipeInteractions;
