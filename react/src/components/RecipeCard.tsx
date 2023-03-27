import {
  Card,
  CardHeader,
  Box,
  CardMedia,
  Typography,
  CardContent,
  Stack,
  Chip,
  CardActions,
  IconButton,
  Button,
  Divider,
} from '@mui/material';
import * as React from 'react';
import { Recipe } from '../types/Recipe';
import RecipeCardInfo from './RecipeCardInfo';
import FavoriteButton from './FavoriteButton';
import CookedButton from './CookedButton';
import ViewRecipeButton from './ViewRecipeButton';
import RecipeInteractions from './RecipeInteractions';
import theme from '../themes/theme';

type RecipeCardProps = React.PropsWithChildren<{
  recipe: Recipe;
  headText?: string;
  subText?: string;
  mediaHeight: number;
}>;

const RecipeCard: React.FunctionComponent<RecipeCardProps> = (props) => {
  return (
    <Card className="recipe-card-item" elevation={3}>
      <CardHeader
        title={props.headText}
        subheader={props.subText}
        subheaderTypographyProps={{ fontWeight: 700 }}
        sx={{
          textTransform: 'capitalize',
          backgroundColor: theme.palette.primary.light,
          paddingY: 1,
        }}
      />
      <Box sx={{ position: 'relative' }}>
        <CardMedia
          component="img"
          height={props.mediaHeight}
          image={props.recipe.imageUrl}
          alt={props.recipe.title}
        />
        <Box
          sx={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            width: '100%',
            bgcolor: 'rgba(0, 0, 0, 0.34)',
            color: 'white',
            padding: '10px',
          }}
        >
          <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
            {props.recipe.title}
          </Typography>
        </Box>
      </Box>
      <RecipeCardInfo recipe={props.recipe} />
      {props.children && (
        <CardContent sx={{ paddingTop: 0.5 }}>
          <Divider flexItem sx={{ marginBottom: 1 }} />
          {props.children}
        </CardContent>
      )}
      <CardActions>
        <RecipeInteractions size="small" recipe={props.recipe} />
      </CardActions>
    </Card>
  );
};

export default RecipeCard;
