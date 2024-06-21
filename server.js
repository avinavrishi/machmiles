const express = require('express');
const axios = require('axios');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(express.json());
app.use(express.static('public'));

// Endpoint to serve the sitemap
app.get('/sitemap.xml', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'sitemap.xml'));
});

app.get('/', (req, res) => {
  res.render('pages/index');
});

app.get('/autocomplete', async (req, res) => {
  const { query } = req.query;

  const options = {
    method: 'GET',
    url: 'https://agoda-com.p.rapidapi.com/flights/auto-complete',
    params: { query: query },
    headers: {
      'x-rapidapi-key': process.env.RAPIDAPI_KEY,
      'x-rapidapi-host': process.env.RAPIDAPI_HOST
    }
  };

  try {
    const response = await axios.request(options);
    const suggestions = [];

    response.data.data.forEach(item => {
      // Add item itself to the suggestions
      // suggestions.push({
      //   name: item.name,
      //   code: item.iata
      // });

      // Add each airport in the item's airports list
      if (item.airports && item.airports.length > 0) {
        item.airports.forEach(airport => {
          suggestions.push({
            name: airport.name,
            code: airport.code
          });
        });
      }
    });

    res.json(suggestions);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});



app.get('/search-flights', async (req, res) => {
  const { flying_from, flying_to, departure_date, adults, children, infants, return_date } = req.query;

  const options = {
      method: 'GET',
      url: 'https://agoda-com.p.rapidapi.com/flights/search-one-way',
      params: {
          origin: flying_from,
          destination: flying_to,
          departureDate: departure_date,
          adults: adults,
          children: children,
          infants: infants
      },
      headers: {
          'x-rapidapi-key': process.env.RAPIDAPI_KEY,
          'x-rapidapi-host': process.env.RAPIDAPI_HOST
      }
  };

  try {
      const response = await axios.request(options);
      const bundles = response.data.data.bundles || [];

      console.log(response.data.data);
      console.log("==================")
      // Log keys of each bundle object
      bundles.forEach((bundle, index) => {
          console.log(`Bundle ${index + 1} keys:`);
          console.log(Object.keys(bundle));
      });

      res.render('pages/results', { bundles });
  } catch (error) {
      console.error(error);
      res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
