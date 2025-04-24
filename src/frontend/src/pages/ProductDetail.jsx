import { useState, useEffect } from "react";
import { useParams, useLocation, useNavigate } from "react-router-dom";
import { 
  Container, 
  Grid, 
  Typography, 
  Box, 
  Button, 
  Divider, 
  Paper, 
  Tabs, 
  Tab, 
  Card, 
  CardMedia, 
  Breadcrumbs, 
  Link, 
  List, 
  ListItem, 
  ListItemIcon, 
  ListItemText,
  TextField,
  IconButton
} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import ProductCard from "../components/ProductCard";
import FilterDrawer from "../components/FilterDrawer";


function ProductDetail() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [tabValue, setTabValue] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [selectedFilters, setSelectedFilters] = useState({
    sugar: false,
    calories: false,
    "saturated fat": false,
    "salt per 100": false,
    ultraprocessed: false,
    nns: false
  });
  
  // Hardcoded features for demo - would come from API in real app
  const productFeatures = [
    "Non-GMO",
    "Organic",
    "Sustainably Sourced",
    "Gluten Free"
  ];
  
  // // Related products - would come from API in real app
  // const relatedProducts = [
  //   { id: 1, name: "Organic Apples", price: 3.99, image: "/images/products/apples.jpg" },
  //   { id: 2, name: "Fresh Strawberries", price: 4.99, image: "/images/products/strawberries.jpg" },
  //   { id: 3, name: "Organic Bananas", price: 1.99, image: "/images/products/bananas.jpg" }
  // ];
  
  const [relatedProducts, setRelatedProducts] = useState([]);

  useEffect(() => {
    const fetchRelatedProducts = async () => {
      try {
        const response = await fetch("http://localhost:8000/recommendations", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            product_name: product.name,
            column_name: "sugar",
          })
        });

        if (!response.ok) throw new Error("Failed to fetch recommendations!");
        const data = await response.json();
        console.log(data)

        setRelatedProducts(data.products)

      } catch (error) {
        console.error("Error fetching related products:", error);
      }
    };

    if (product) {
      fetchRelatedProducts();
    }
  }, [product, "sugar"]
);


  useEffect(() => {
    // If product data was passed via navigation state, use it
    if (location.state) {
      setProduct({
        ...location.state,
        description: "This premium product is carefully selected for quality and freshness. It's part of our commitment to bringing you the best grocery options to support a healthy lifestyle.",

        // this is static/mock data we need to exchange with actual data
        nutrition: {
          calories: "120 per serving",
          servingSize: "100g",
          protein: "2g",
          fat: "0.5g",
          carbs: "25g",
          fiber: "3g"
        }
      });
      setLoading(false);
    } else {
      // Fetch product details from API
      const fetchProductDetails = async () => {
        try {
          const response = await fetch(`http://127.0.0.1:8000/product-detail/${id}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
          });
          
          if (!response.ok) throw new Error("Failed to fetch product details");
          
          const data = await response.json();
          console.log(data);
          setProduct({
            ...data,
            description: data.description || "Product description not available",
            nutrition: data.nutrition || {
              calories: "Information not available",
              servingSize: "Information not available",
              protein: "Information not available",
              fat: "Information not available",
              carbs: "Information not available",
              fiber: "Information not available"
            }
          });
        } catch (error) {
          console.error("Error fetching product details:", error);
        } finally {
          setLoading(false);
        }
      };
      
      fetchProductDetails();
    }
  }, [id, location.state]);
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const handleQuantityChange = (event) => {
    const value = parseInt(event.target.value);
    if (!isNaN(value) && value > 0) {
      setQuantity(value);
    }
  };
  
  const incrementQuantity = () => {
    setQuantity(prevQuantity => prevQuantity + 1);
  };
  
  const decrementQuantity = () => {
    if (quantity > 1) {
      setQuantity(prevQuantity => prevQuantity - 1);
    }
  };
  
  if (loading) {
    return (
      <Container sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h5">Loading product details...</Typography>
      </Container>
    );
  }
  
  if (!product) {
    return (
      <Container sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h5">Product not found</Typography>
        <Button 
          variant="contained" 
          sx={{ mt: 2 }}
          onClick={() => navigate('/')}
        >
          Return to Home
        </Button>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs 
        separator={<NavigateNextIcon fontSize="small" />} 
        aria-label="breadcrumb"
        sx={{ mb: 3 }}
      >
        <Link underline="hover" color="inherit" onClick={() => navigate('/')} sx={{ cursor: 'pointer' }}>
          Home
        </Link>
        <Typography color="text.primary">{product.name}</Typography>
      </Breadcrumbs>
      
      {/* Product Details Section */}
      <Grid container spacing={4}>
        {/* Product Image */}
        <Grid item xs={12} md={6}>
          <Paper 
            elevation={0} 
            sx={{ 
              height: '100%', 
              display: 'flex', 
              justifyContent: 'center', 
              alignItems: 'center',
              backgroundColor: '#f5f5f5',
              borderRadius: 2,
              p: 2
            }}
          >
            <Box 
              component="img"
              sx={{
                maxHeight: '400px',
                maxWidth: '100%',
                objectFit: 'contain'
              }}
              src={product.image || "/images/product-placeholder.jpg"}
              alt={product.name}
            />
          </Paper>
        </Grid>
        
        {/* Product Information */}
        <Grid item xs={12} md={6}>
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontFamily: 'Garamond, serif' }}>
            {product.name}
          </Typography>
          
          <Typography variant="h5" color="primary" sx={{ mb: 2, fontWeight: 'bold' }}>
            ${product.price ? product.price.toFixed(2) : "Price not available"}
          </Typography>
          
          <Typography variant="body1" paragraph>
            {product.description}
          </Typography>
          
          {/* Features List */}
          <List dense>
            {productFeatures.map((feature, index) => (
              <ListItem key={index} disablePadding sx={{ py: 0.5 }}>
                <ListItemIcon sx={{ minWidth: '30px' }}>
                  <CheckCircleOutlineIcon color="success" fontSize="small" />
                </ListItemIcon>
                <ListItemText primary={feature} />
              </ListItem>
            ))}
          </List>
          
          <Divider sx={{ my: 2 }} />
          
          {/* Quantity Selector */}
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Typography variant="body1" sx={{ mr: 2 }}>Quantity:</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <IconButton size="small" onClick={decrementQuantity}>
                <RemoveIcon fontSize="small" />
              </IconButton>
              <TextField
                size="small"
                inputProps={{ 
                  min: 1, 
                  style: { textAlign: 'center' }
                }}
                value={quantity}
                onChange={handleQuantityChange}
                sx={{ width: '60px', mx: 1 }}
              />
              <IconButton size="small" onClick={incrementQuantity}>
                <AddIcon fontSize="small" />
              </IconButton>
            </Box>
          </Box>
          
          {/* Add to Cart Button */}
          <Button 
            variant="contained" 
            fullWidth 
            size="large"
            sx={{ 
              backgroundColor: '#4a7c59', 
              '&:hover': { backgroundColor: '#3a6349' },
              py: 1.5
            }}
          >
            Add to Cart
          </Button>
        </Grid>
      </Grid>
      
      {/* Tabs Section */}
      <Box sx={{ mt: 6, mb: 4 }}>
        <Tabs 
          value={tabValue} 
          onChange={handleTabChange}
          centered
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="Description" />
          <Tab label="Nutrition Facts" />
          <Tab label="Reviews" />
        </Tabs>
        
        {/* Tab Panels */}
        <Box sx={{ py: 3 }}>
          {tabValue === 0 && (
            <Typography variant="body1" paragraph>
              {product.description}
              <br/><br/>
              Our products are sourced from trusted farmers and suppliers who share our commitment to quality and sustainability. We believe that what you put in your body matters, and we're dedicated to providing options that support your well-being and the health of our planet.
            </Typography>
          )}
          {tabValue === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom>Nutrition Information</Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Serving Size</Typography>
                    <Typography variant="body1">{product.nutrition.servingSize}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Calories</Typography>
                    <Typography variant="body1">{product.nutrition.calories}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Protein</Typography>
                    <Typography variant="body1">{product.nutrition.protein}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Total Fat</Typography>
                    <Typography variant="body1">{product.nutrition.fat}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Total Carbohydrates</Typography>
                    <Typography variant="body1">{product.nutrition.carbs}</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Paper variant="outlined" sx={{ p: 2 }}>
                    <Typography variant="subtitle2">Dietary Fiber</Typography>
                    <Typography variant="body1">{product.nutrition.fiber}</Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Box>
          )}
          {tabValue === 2 && (
            <Box>
              <Typography variant="body1" paragraph>
                No reviews yet. Be the first to review this product!
              </Typography>
              <Button variant="outlined">Write a Review</Button>
            </Box>
          )}
        </Box>
      </Box>
      
      {/* Related Products Section */}
      <Grid container spacing={3}>
        {relatedProducts.map((product, index) => (
          <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
            <ProductCard
              name={product.product || "Unknown Product"}
              price={product.price || 0}
              image={product.image}
              onClick={() =>
                navigate(`/product/${encodeURIComponent(product.product)}`, {
                  state: {
                    name: product.product,
                    price: product.price,
                    image: product.image,
                  },
                })
              }
            />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default ProductDetail;