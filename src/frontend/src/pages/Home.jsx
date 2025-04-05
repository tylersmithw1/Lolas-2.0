import { useState } from "react";
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia, 
  Button, 
  TextField, 
  IconButton, 
  Drawer, 
  Checkbox, 
  FormControlLabel, 
  FormGroup, 
  Divider, 
  InputAdornment,
  CardActionArea
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import FilterListIcon from '@mui/icons-material/FilterList';

import ProductCard from "../components/ProductCard";

function Home() {
  const [products, setProducts] = useState([]);
  // filter 
  const [searchQuery, setSearchQuery] = useState("");
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [allProducts, setAllProducts] = useState([]);
  const [selectedFilters, setSelectedFilters] = useState({
    vegan: false,
    glutenFree: false,
    organic: false,
    nonGMO: false,
    lowSodium: false
  });

  //categories
  const categories = [
    { name: "Fruits & Vegetables", image: "/images/categories/fruits-vegetables.jpg" },
    { name: "Dairy & Eggs", image: "/images/categories/dairy-eggs.jpg" },
    { name: "Bakery", image: "/images/categories/bakery.jpg" },
    { name: "Pantry Staples", image: "/images/categories/pantry.jpg" },
    { name: "Beverages", image: "/images/categories/beverages.jpg" },
    { name: "Snacks", image: "/images/categories/snacks.jpg" }
  ];

  // Fetch products when search query is submitted
  const fetchProducts = async (query) => {
    try {
      const response = await fetch("http://localhost:8000/grocery", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ search_string: query }),
      });

      if (!response.ok) throw new Error("Failed to fetch");

      const data = await response.json();
      console.log(data)
      setProducts(data.products || []);  // Update the state directly
      setAllProducts(data.products || []);

    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchProducts(searchQuery);
  };

  const handleFilterChange = (event) => {
    setSelectedFilters({
      ...selectedFilters,
      [event.target.name]: event.target.checked
    });
  };

  const toggleFilter = () => {
    setIsFilterOpen(!isFilterOpen);
  };


  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* Navigation and Search Bar */}
      <AppBar position="static" color="default" elevation={1} sx={{ backgroundColor: 'white' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontFamily: 'Garamond, serif', fontWeight: 'bold' }}>
            Lola's Grocery
          </Typography>
          
          <Box component="form" onSubmit={handleSearchSubmit} sx={{ display: 'flex', alignItems: 'center' }}>
            <TextField
              variant="outlined"
              size="small"
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              sx={{ mr: 1, width: '250px' }}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton type="submit" edge="end">
                      <SearchIcon />
                    </IconButton>
                  </InputAdornment>
                )
              }}
            />
            <IconButton onClick={toggleFilter}>
              <FilterListIcon />
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Filter Drawer */}
      <Drawer
        anchor="right"
        open={isFilterOpen}
        onClose={toggleFilter}
      >
        <Box sx={{ width: 250, padding: 2 }}>
          <Typography variant="h6" gutterBottom>
            Dietary Preferences
          </Typography>
          <FormGroup>
            <FormControlLabel 
              control={<Checkbox checked={selectedFilters.vegan} onChange={handleFilterChange} name="vegan" />} 
              label="Vegan" 
            />
            <FormControlLabel 
              control={<Checkbox checked={selectedFilters.glutenFree} onChange={handleFilterChange} name="glutenFree" />} 
              label="Gluten Free" 
            />
            <FormControlLabel 
              control={<Checkbox checked={selectedFilters.organic} onChange={handleFilterChange} name="organic" />} 
              label="Organic" 
            />
            <FormControlLabel 
              control={<Checkbox checked={selectedFilters.nonGMO} onChange={handleFilterChange} name="nonGMO" />} 
              label="Non-GMO" 
            />
            <FormControlLabel 
              control={<Checkbox checked={selectedFilters.lowSodium} onChange={handleFilterChange} name="lowSodium" />}
              label="Low Sodium" 
            />
          </FormGroup>
          <Box sx={{ mt: 2 }}>
            <Button 
              variant="contained" 
              fullWidth 
              onClick={() => {
                fetchProducts(searchQuery);
                toggleFilter();
              }}
            >
              Apply Filters
            </Button>
          </Box>
        </Box>
      </Drawer>

      {/* Main Content */}
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        {products.length > 0 ? (
          /* Search Results Page */
          <Box>
            <Typography variant="h4" gutterBottom>
              Healthiest Options for '{searchQuery}'
            </Typography>
            
            <Divider sx={{ mb: 3 }} />
            <Grid container spacing={3}>
              {products.map((product, index) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                  <ProductCard
                    name={product.product || "Unknown Product"}
                    price={product.price || 0}
                  />
                </Grid>
              ))}
            </Grid>
          </Box>
        ) : (
          /* Homepage Content */
          <Box>
            {/* Hero Section */}
            <Box 
              sx={{ 
                display: 'flex', 
                flexDirection: { xs: 'column', md: 'row' },
                alignItems: 'center',
                backgroundColor: '#f8f9fa',
                borderRadius: 2,
                overflow: 'hidden',
                mb: 6,
                mt: 2
              }}
            >
              <Box 
                sx={{ 
                  width: { xs: '100%', md: '50%' }, 
                  p: { xs: 3, md: 6 }
                }}
              >
                <Typography variant="h3" component="h1" sx={{ fontFamily: 'Garamond, serif', mb: 2 }}>
                  Fresh Ingredients for Healthy Living
                </Typography>
                <Typography variant="body1" paragraph>
                  At Lola's, we believe in providing the freshest, highest-quality grocery options to help you live your healthiest life. Our carefully curated selection prioritizes organic, locally-sourced products whenever possible.
                </Typography>
                <Button 
                  variant="contained" 
                  size="large" 
                  sx={{ 
                    backgroundColor: '#4a7c59', 
                    '&:hover': { backgroundColor: '#3a6349' } 
                  }}
                >
                  Shop Now
                </Button>
              </Box>
              <Box 
                sx={{ 
                  width: { xs: '100%', md: '50%' },
                  height: { xs: '200px', md: '400px' },
                  backgroundImage: 'url(/images/hero-veggies.jpg)',
                  backgroundSize: 'cover',
                  backgroundPosition: 'center'
                }}
              />
            </Box>

            {/* Categories Section */}
            <Box sx={{ mb: 6 }}>
              <Typography variant="h4" component="h2" sx={{ mb: 3, fontFamily: 'Garamond, serif' }}>
                Shop by Category
              </Typography>
              <Grid container spacing={3}>
                {categories.map((category, index) => (
                  <Grid item xs={6} sm={4} md={2} key={index}>
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                      <CardActionArea>
                        <CardMedia
                          component="div"
                          sx={{ height: 140, backgroundSize: 'cover' }}
                          image={category.image}
                          title={category.name}
                        />
                        <CardContent>
                          <Typography variant="subtitle1" component="h3" align="center">
                            {category.name}
                          </Typography>
                        </CardContent>
                      </CardActionArea>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          </Box>
        )}
      </Container>
    </Box>
  );
}


export default Home;
