import { IconButton, Tooltip } from '@mui/material';
import * as React from 'react';
import FavoriteOutlinedIcon from '@mui/icons-material/FavoriteOutlined';
import FavoriteBorderOutlinedIcon from '@mui/icons-material/FavoriteBorderOutlined';

type FavoriteButtonProps = {
  filled: boolean | unknown;
  size: 'small' | 'medium' | 'large';
  onClick: (event: React.MouseEvent<HTMLElement>) => void;
};

const FavoriteButton: React.FunctionComponent<FavoriteButtonProps> = (
  props
) => {
  if (props.filled)
    return (
      <Tooltip title="Remove recipe from favotires">
        <IconButton size={props.size} color="love" onClick={props.onClick}>
          <FavoriteOutlinedIcon />
        </IconButton>
      </Tooltip>
    );
  else
    return (
      <Tooltip title="Add recipe to favorites">
        <IconButton size={props.size} color="love" onClick={props.onClick}>
          <FavoriteBorderOutlinedIcon />
        </IconButton>
      </Tooltip>
    );
};

export default FavoriteButton;
