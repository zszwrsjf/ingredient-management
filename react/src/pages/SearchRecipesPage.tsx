import * as React from 'react';
import { useLocation } from 'react-router-dom';
import { Ingredient } from '../types/Ingredient';
import { useFetchRecipes } from '../hooks/useFetchRecipes';
import LoadingOverlay from '../components/LoadingOverlay';
import RecipeItemList from '../components/RecipeItemList';
import {
  Box,
  Button,
  Chip,
  Grid,
  Paper,
  Stack,
  Typography,
} from '@mui/material';
import AutoCompleteIngredient from '../components/form/ingredient/AutoCompleteIngredient';
import { FormProvider, useForm } from 'react-hook-form';
import { useFetchIngredients } from '../hooks/useFetchIngredients';
import { InputRadioGroup } from '../components/form/InputRadioGroup';

type Inputs = {
  ingredient: Ingredient;
  anyFilter: 'any' | 'exact';
  strictFilter: 'strict' | 'relaxed';
};

const SearchRecipesPage: React.FunctionComponent = () => {
  const location = useLocation();
  const methods = useForm<Inputs>();
  const watchAnyFilter = methods.watch('anyFilter');
  const watchStrictFilter = methods.watch('strictFilter');

  // selectedIngredients is a list of numbers (ids) of selected ingredients
  const [ingredientIds, setIngredientIds] = React.useState<number[]>(() => {
    const ids: number[] = [];
    const obj = JSON.parse(location.state);
    for (const key in obj) {
      if (obj[key]) {
        ids.push(Number(key));
      }
    }
    return ids;
  });

  const { recipes, onChangeRecipes, isLoading } = useFetchRecipes();
  const { ingredients, onChangeIngredients } = useFetchIngredients();

  const executeSearch = () => {
    onChangeRecipes(
      ingredientIds,
      watchAnyFilter,
      watchStrictFilter === 'strict'
    );
  };

  /// execute search on the initial render, potentially using the ingredients
  /// selected on the "My Ingredients" page
  React.useEffect(() => {
    executeSearch();
  }, []);

  const submitHandler = (event: React.FormEvent) => {
    event.preventDefault();
    methods.handleSubmit(executeSearch)();
  };

  React.useEffect(() => {
    onChangeIngredients(ingredientIds);
    // want to update the recipe list every time selected ingredients are changed.
    // Jsonfy the array in order to pass it to dependency list
  }, [JSON.stringify(ingredientIds)]);

  const onIngredientSelect = (i: Ingredient) => {
    setIngredientIds((prevIngredientIds) => [...prevIngredientIds, i.id]);
  };

  const removeIngredient = (id: number) => {
    setIngredientIds((prevIngredientIds) =>
      prevIngredientIds.filter((i) => i !== id)
    );
  };

  return (
    <React.Fragment>
      <LoadingOverlay isLoading={isLoading} />
      <Typography component="div" variant="h3">
        Search Recipes
      </Typography>
      <FormProvider {...methods}>
        <Grid
          container
          className="recipe-search-options"
          component="form"
          spacing={2}
          sx={{ marginY: 2 }}
          onSubmit={submitHandler}
        >
          <Grid item xs={12} md={6}>
            <AutoCompleteIngredient
              onSelect={onIngredientSelect}
              clearAfterSelect
            />
          </Grid>
          <Grid
            item
            xs={6}
            md={3}
            sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
          >
            <Box>
              <InputRadioGroup
                datatip={['use any ingredients selected', 'use all ingredients selected']}
                default="any"
                name="anyFilter"
                options={['any', 'exact']}
                row
              />
            </Box>
          </Grid>
          <Grid
            item
            xs={6}
            md={3}
            sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
          >
            <Box>
              <InputRadioGroup
                datatip={['no more ingredients other than selected', 'more ingredients other than selected']}
                default="relaxed"
                name="strictFilter"
                options={['strict', 'relaxed']}
                row
              />
            </Box>
          </Grid>
          <Grid item xs={12}>
            {ingredients.length > 0 && (
              <Paper sx={{ padding: 2 }} variant="outlined">
                <Stack
                  direction="row"
                  sx={{ flexWrap: 'wrap', columnGap: 2, rowGap: 1 }}
                >
                  {ingredients.map((ig) => {
                    return (
                      <Chip
                        key={ig.id}
                        label={ig.name.toUpperCase()}
                        onDelete={() => removeIngredient(ig.id)}
                        sx={{ fontSize: 16 }}
                      />
                    );
                  })}
                </Stack>
              </Paper>
            )}
          </Grid>
          <Grid
            item
            xs={12}
            sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
          >
            <Button
              type="submit"
              variant="contained"
              color="secondary"
              sx={{ flex: '1', mb: 2 }}
            >
              SEARCH
            </Button>
          </Grid>
        </Grid>
      </FormProvider>
      <RecipeItemList
        recipes={recipes}
        displayNutrition={true}
        displayTags={true}
      />
    </React.Fragment>
  );
};

export default SearchRecipesPage;
