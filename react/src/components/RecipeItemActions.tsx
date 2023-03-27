import {
  Grid,
  Stack,
  Button,
  Typography,
  Box,
  IconButton,
  Tooltip,
  Divider,
} from '@mui/material';
import type { FC } from 'react';
import { Recipe } from '../types/Recipe';
import KeyboardArrowRightOutlinedIcon from '@mui/icons-material/KeyboardArrowRightOutlined';
import PersonOutlineOutlinedIcon from '@mui/icons-material/PersonOutlineOutlined';
import SentimentSatisfiedAltOutlinedIcon from '@mui/icons-material/SentimentSatisfiedAltOutlined';
import ListAltOutlinedIcon from '@mui/icons-material/ListAltOutlined';
import FavoriteButton from './FavoriteButton';
import RecipeInteractions from './RecipeInteractions';

export const RecipeItemActions: FC<{ recipe: Recipe }> = ({ recipe }) => {
  return (
    <Box className="recipe-item-actions" paddingX={2} paddingBottom={2}>
      <Grid
        container
        alignContent="space-between"
        alignItems="center"
        rowSpacing={2}
        columnSpacing={0}
      >
        <Grid item xs={12} md={8}>
          <Stack direction="row" spacing={2}>
            <Typography
              variant="body1"
              sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
            >
              <PersonOutlineOutlinedIcon sx={{ marginRight: 0.5 }} />
              {recipe.allCooked} users cooked
            </Typography>
            <Divider orientation="vertical" variant="middle" flexItem />
            <Typography
              variant="body1"
              sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
            >
              <SentimentSatisfiedAltOutlinedIcon sx={{ marginRight: 0.5 }} />
              {recipe.allFavorite} users liked
            </Typography>
            <Divider orientation="vertical" variant="middle" flexItem />
            <Typography
              variant="body1"
              sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
            >
              <ListAltOutlinedIcon sx={{ marginRight: 0.5 }} />
              {recipe.numIngredients} total ingredients
            </Typography>
          </Stack>
        </Grid>
        <Grid item xs={12} md={4}>
          <RecipeInteractions size="large" recipe={recipe} />
        </Grid>
      </Grid>
    </Box>
  );
};
