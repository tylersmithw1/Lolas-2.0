import { useNavigate } from "react-router-dom";
import { Card, CardActionArea, CardContent, CardMedia, Typography, Box, IconButton } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

function ProductCard({ name, price, image, healthRating, serving_size, calories, protein, total_fat, total_carbohydrates, dietary_fiber, sugar, sodium}) {
  const navigate = useNavigate();

  const renderHealthRating = () => {
    return (
      <Box sx={{ display: 'flex', mb: 1 }}>
        {[...Array(5)].map((_, index) => (
          <Box
            key={index}
            sx={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              backgroundColor: '#ccc',
              marginRight: 0.5,
            }}
          />
        ))}
      </Box>
    );
  };

  return (
    <Card sx={{ width: 220, height: 300, borderRadius: 2, overflow: 'hidden', boxShadow: 2, position: 'relative' }}>
      <CardActionArea
        sx={{ display: 'flex', flexDirection: 'column', alignItems: 'stretch' }}
        onClick={() => {
          navigate(`/product/${encodeURIComponent(name)}`, {
            state: { name, price, image, serving_size, calories, protein, total_fat, total_carbohydrates, dietary_fiber, sugar, sodium },
          });
          setTimeout(() => window.scrollTo(0, 0), 0);
        }}
        
        
      >
        <CardMedia
          component="img"
          image={image}
          alt={name}
          sx={{ width: '100%', height: 170, objectFit: 'cover', backgroundColor: '#f5f5f5' }}
        />
        <CardContent sx={{ padding: 1, flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          <Typography gutterBottom variant="body2" sx={{ fontWeight: 'bold', fontSize: 14 }}>
            {name}
          </Typography>
          {renderHealthRating()}
          <Typography variant="body2" color="text.secondary" sx={{ marginBottom: 1 }}>
            ${price ? price.toFixed(2) : "0.00"}
          </Typography>
        </CardContent>
      </CardActionArea>
      
      <IconButton
        sx={{ position: 'absolute', bottom: 8, right: 8, backgroundColor: '#4CAF50', color: 'white', '&:hover': { backgroundColor: '#45a049' } }}
        onClick={() => navigate('/cart')}
      >
        <AddIcon />
      </IconButton>
    </Card>
  );
}

export default ProductCard;
