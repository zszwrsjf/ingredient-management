import { Stack, Typography, Divider, Paper, Box, Grid } from '@mui/material';
import * as React from 'react';
import SoupKitchenOutlinedIcon from '@mui/icons-material/SoupKitchenOutlined';
import SentimentSatisfiedAltOutlinedIcon from '@mui/icons-material/SentimentSatisfiedAltOutlined';
import KitchenOutlinedIcon from '@mui/icons-material/KitchenOutlined';
import { User } from '../types/User';
import { UserInfo } from '../types/UserInfo';

export interface UserBasicInfoProps {
  title: string;
  user?: User;
  userInfo?: UserInfo;
}

export function UserBasicInfo(props: UserBasicInfoProps) {
  return (
    <Stack direction="column" spacing={2}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={'auto'}>
          <Typography variant="h3">{props.user?.username}</Typography>
        </Grid>
        <Grid item xs={12} md>
          <Typography variant="h3" sx={{ fontWeight: 100 }}>
            {props.title}
          </Typography>
        </Grid>
      </Grid>
      {props.userInfo && (
        <Box className="user-info-stats">
          <Stack direction="row" spacing={2}>
            <Typography
              variant="h6"
              sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
            >
              <SoupKitchenOutlinedIcon sx={{ marginRight: 0.5 }} />
              {props.userInfo ? props.userInfo.allCooked : 0} Recipes Cooked
            </Typography>
            <Divider orientation="vertical" variant="middle" flexItem />
            <Typography
              variant="h6"
              sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
            >
              <SentimentSatisfiedAltOutlinedIcon sx={{ marginRight: 0.5 }} />
              {props.userInfo ? props.userInfo.allLiked : 0} Recipes Liked
            </Typography>
            <Divider orientation="vertical" variant="middle" flexItem />
            <Typography
              variant="h6"
              sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap' }}
            >
              <KitchenOutlinedIcon sx={{ marginRight: 0.5 }} />
              {props.userInfo ? props.userInfo.allIngredients : 0} Active
              Ingredients
            </Typography>
          </Stack>
        </Box>
      )}
    </Stack>
  );
}
