import { Theme } from '@emotion/react';
import { Box, Chip, Typography } from '@mui/material';
import { Stack } from '@mui/system';
import type { FC } from 'react';
import { Recipe } from '../types/Recipe';

const TagBlockTheme: Theme = {
  padding: 2,
  backgroundColor: 'grey.100',
  boxShadow: 'inset 0 7px 9px -7px rgba(0,0,0,0.4)',
  display: 'flex',
  alignItems: 'center',
  flexWrap: 'wrap',
};

export const RecipeItemTags: FC<{ recipe: Recipe }> = ({ recipe }) => {
  return (
    <Box className="recipe-item-tags" sx={TagBlockTheme}>
      <Stack direction="row" sx={{ flexWrap: 'wrap', columnGap: 2, rowGap: 1 }}>
        {recipe.tags &&
          recipe.tags.map((tag) => (
            <Chip
              key={tag.id}
              label={tag.name.replaceAll('-', ' ').toUpperCase()}
            />
          ))}
        {!recipe.tags ||
          (recipe.tags.length <= 0 && (
            <Typography variant="body1">No tags available.</Typography>
          ))}
      </Stack>
    </Box>
  );
};
