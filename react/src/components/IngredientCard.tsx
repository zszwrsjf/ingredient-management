import type { FC } from 'react';
import type { UserIngredient } from '../types/UserIngredient';
import { ShelfLifeDaysBar } from './ShelfLifeDaysBar';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import theme from '../themes/theme';
import { Divider, IconButton, Stack, Tooltip } from '@mui/material';
import NoMealsIcon from '@mui/icons-material/NoMeals';
import ClearIcon from '@mui/icons-material/Clear';
import { round, trim_to_length } from '../util/misc';
import { useAxios } from '../hooks/useAxios';

type IngredientCardProps = {
  onAction: () => void;
  userIngredient: UserIngredient;
  checkbox: JSX.Element;
};

export const IngredientCard: FC<IngredientCardProps> = (props) => {
  const { api } = useAxios();
  const { userIngredient, checkbox, onAction } = props;
  const { createdDate, expirationDate, ingredient } = userIngredient;
  const { name, imageUrl } = ingredient;

  const today = new Date();
  const initialDate = new Date(createdDate);
  const expireAt = new Date(expirationDate);

  const shelfLifeDays = Math.max(
    (expireAt.getTime() - today.getTime()) / 1000 / 60 / 60 / 24,
    0
  );
  const initShelfLifeDays = Math.max(
    (expireAt.getTime() - initialDate.getTime()) / 1000 / 60 / 60 / 24,
    0
  );

  const shelfLifeRatio = Math.min(
    (shelfLifeDays / initShelfLifeDays) * 100,
    100
  );

  const cardHeight = 148;

  return (
    <Card sx={{ display: 'flex' }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
        }}
      >
        <Stack direction="column" spacing={0}>
          <Box sx={{ height: (2 * cardHeight) / 3 }}>{checkbox}</Box>
          <Box sx={{ height: cardHeight / 3 }}>
            <IconButton
              sx={{
                color: 'white',
                opacity: 0.8,
                backgroundColor: theme.palette.error.light,
                borderRadius: 0,
                width: '100%',
                height: '105%',
                '&:hover': {
                  color: 'white',
                  backgroundColor: theme.palette.error.dark,
                  opacity: 1.0,
                },
              }}
              onClick={async () => {
                try {
                  await api.put('/user/ingredients', {
                    user_ingredient_id: userIngredient.id,
                    consumed: true,
                  });
                  onAction();
                } catch (err) {
                  console.log(err);
                }
              }}
            >
              <ClearIcon />
            </IconButton>
          </Box>
        </Stack>
      </Box>
      <CardMedia
        component="img"
        sx={{
          width: 120,
          height: cardHeight,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          overflow: 'hidden',
        }}
        image={imageUrl}
        alt={`${name} image`}
      />
      <Box
        sx={{
          display: 'flex',
          flex: '1 0 auto',
          justifyContent: 'space-between',
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            flexGrow: 1,
            width: 160,
            pr: 2,
          }}
        >
          <CardContent
            sx={{
              paddingRight: 0,
              '&:last-child': { paddingBottom: 2 },
              height: cardHeight,
            }}
          >
            <Tooltip title={name.toUpperCase()} arrow>
              <Typography
                align="left"
                component="div"
                variant="h6"
                sx={{ textTransform: 'capitalize', lineHeight: '120%' }}
              >
                {trim_to_length(name, 25)}
              </Typography>
            </Tooltip>
            <Divider sx={{ my: 1 }} flexItem />
            <ShelfLifeDaysBar
              variant="determinate"
              value={shelfLifeRatio}
              dayleft={shelfLifeDays}
            />
            <Typography align="left" component="div" variant="body2">
              {shelfLifeDays > 1
                ? round(shelfLifeDays, 0)
                : round(shelfLifeDays, 1)}{' '}
              day(s) remaining
            </Typography>
          </CardContent>
        </Box>
      </Box>
    </Card>
  );
};
